#!/usr/bin/env python3

import time
from rpi_ws281x import PixelStrip, Color
import argparse
import threading

# LED strip configuration:
LED_COUNT = 300        # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53



class LED:

    def __init__(self, brightness=1.0):

        self.strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        self.strip.begin()

        self.brightness = brightness
        if self.brightness < 0:
            self.brightness = 0
        elif self.brightness > 1:
            self.brightness = 1
        
        self.current_pattern = None
        self.stop_event = threading.Event()

    def start_pattern(self, pattern_func):
        self.stop_event.clear()
        self.current_pattern = threading.Thread(target=pattern_func)
        self.current_pattern.start()


    def stop_pattern(self):
        if self.current_pattern:
            self.stop_event.set()
            # self.current_pattern.join()
            self.current_pattern = None


    def solidColor(self, color):
        """Fill the entire strip with a single color."""
        color = Color(*color)
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
        self.strip.show()


    def colorWipe(self, color, wait_ms=50):
        """Wipe color across display a pixel at a time."""
        color = Color(*color)
        while not self.stop_event.is_set():
            for i in range(self.strip.numPixels()):
                if self.stop_event.is_set():
                    break
                self.strip.setPixelColor(i, color)
                self.strip.show()
                time.sleep(wait_ms / 1000.0)
            for i in range(self.strip.numPixels()):
                if self.stop_event.is_set():
                    break
                self.strip.setPixelColor(i, Color(0, 0, 0))
                self.strip.show()
                time.sleep(wait_ms / 1000.0)


    def theaterChase(self, color, wait_ms=50, iterations=10):
        """Movie theater light style chaser animation."""
        color = Color(*color)
        while not self.stop_event.is_set():
            for q in range(3):
                for i in range(0, self.strip.numPixels(), 3):
                    if self.stop_event.is_set():
                        break
                    self.strip.setPixelColor(i + q, color)
                self.strip.show()
                time.sleep(wait_ms / 1000.0)
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, 0)


    def wheel(self, pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            R, G, B = pos * 3, 255 - pos * 3, 0
            return Color(R, G, B)
        elif pos < 170:
            pos -= 85
            R, G, B= 255 - pos * 3, 0, pos * 3
            return Color(R, G, B)
        else:
            pos -= 170
            R, G, B = 0, pos * 3, 255 - pos * 3
            return Color(R, G, B)
    
    def rainbow(self, wait_ms=20, iterations=1):
        """Draw rainbow that fades across all pixels at once."""
        while True:
            for j in range(256 * iterations):
                for i in range(self.strip.numPixels()):
                    self.strip.setPixelColor(i, self.wheel((i + j) & 255))
                    if self.stop_event.is_set():
                        break
                self.strip.show()
                time.sleep(wait_ms / 1000.0)


    def rainbowCycle(self, wait_ms=20, iterations=5):
        """Draw rainbow that uniformly distributes itself across all pixels."""
        while not self.stop_event.is_set():
            for j in range(256 * iterations):
                for i in range(self.strip.numPixels()):
                    self.strip.setPixelColor(i, self.wheel((int(i * 256 / self.strip.numPixels()) + j) & 255))
                if self.stop_event.is_set():
                    return
                self.strip.show()
                time.sleep(wait_ms / 1000.0)
    

    def theaterChaseRainbow(self, wait_ms=50):
        """Rainbow movie theater light style chaser animation."""
        while not self.stop_event.is_set():
            for j in range(256):
                for q in range(3):
                    for i in range(0, self.strip.numPixels(), 3):
                        self.strip.setPixelColor(i + q, self.wheel((i + j) % 255))
                    if self.stop_event.is_set():
                        break
                    self.strip.show()
                    time.sleep(wait_ms / 1000.0)
                    for i in range(0, self.strip.numPixels(), 3):
                        self.strip.setPixelColor(i + q, 0)
        

    def clear(self):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, Color(0, 0, 0))
        self.strip.show()
    

if __name__ == "__main__":
    # create an argparser and add arguments for each of the functions in the LED class
    parser = argparse.ArgumentParser(description="LED strip control")
    parser.add_argument("function", type=str, help="The function to call")
    parser.add_argument("--color", type=str, help="The color to use as comma separated RGB values")
    parser.add_argument("--brightness", type=float, help="The brightness scale", default=1.0)
    args = parser.parse_args()

    led = LED(args.brightness)
    if args.function == "solidColor":
        color = [127, 127, 127]
        if args.color:
            color = [int(c) for c in args.color.split(",")]
        led.solidColor(color)
    elif args.function == "rainbow":
        led.rainbow()
    elif args.function == "rainbowCycle":
        led.rainbowCycle()
    elif args.function == "theaterChase":
        color = [127, 127, 127]
        if args.color:
            color = [int(c) for c in args.color.split(",")]
        led.theaterChase(color)
    elif args.function == "colorWipe":
        color = [127, 127, 127]
        if args.color:
            color = [int(c) for c in args.color.split(",")]
        led.colorWipe(color)
    elif args.function == "theaterChaseRainbow":
        led.theaterChaseRainbow()
    elif args.function == "clear":
        led.clear()
    else:
        print("Invalid function")
        exit(1)