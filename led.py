#!/usr/bin/env python3

import time
from rpi_ws281x import PixelStrip, Color
import argparse
from random import randint
import numpy as np
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

        # self.brightness = brightness
        # if self.brightness < 0:
        #     self.brightness = 0
        # elif self.brightness > 1:
        #     self.brightness = 1
        
        self.current_pattern = "clear"
        self.rgb = [0, 0, 0]
        self.delay_ms = 20

    def solidColor(self, rgb):
        """Fill the entire strip with a single color."""
        self.current_pattern = "solidColor"
        self.rgb = self.threshold_brightness(rgb)
        # self.rgb = rgb
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, Color(*self.rgb))
        self.strip.show()

    def threshold_brightness(self, rgb, threshold=127):
        # Calculate the total brightness of the RGB tuple
        total_brightness = np.mean(rgb)

        # Check if total brightness exceeds the threshold
        if total_brightness > threshold:
            # Calculate the scaling factor to dampen brightness
            scale_factor = threshold / total_brightness

            # Dampen the brightness of each component proportionally
            dampened_rgb = tuple(int(value * scale_factor) for value in rgb)
            return dampened_rgb
        else:
            # If total brightness is below threshold, return the original tuple
            return rgb    

    def colorWipe(self, rgb, delay_ms=50):
        """Wipe color across display a pixel at a time."""
        self.current_pattern = "colorWipe"
        self.rgb = self.threshold_brightness(rgb)
        # self.rgb = rgb
        self.delay_ms = delay_ms
        while True:
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, Color(*self.rgb))
                self.strip.show()
                time.sleep(self.delay_ms / 1000.0)
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, Color(0, 0, 0))
                self.strip.show()
                time.sleep(self.delay_ms / 1000.0)

    def rainbowWipe(self, delay_ms=35):
        """Wipe rainbow across display a pixel at a time."""
        self.current_pattern = "rainbowWipe"
        self.delay_ms = delay_ms
        while True:
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, self.wheel((i) & 255))
                self.strip.show()
                time.sleep(self.delay_ms / 1000.0)
            for i in range(self.strip.numPixels(), 0, -1):
                self.strip.setPixelColor(i, Color(0, 0, 0))
                self.strip.show()
                time.sleep(self.delay_ms / 1000.0)
            for i in range(self.strip.numPixels(), 0, -1):
                self.strip.setPixelColor(i, self.wheel((i) & 255))
                self.strip.show()
                time.sleep(self.delay_ms / 1000.0)
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i,  Color(0, 0, 0))
                self.strip.show()
                time.sleep(self.delay_ms / 1000.0)


    def rainbowWipeAlwaysOn(self, delay_ms=20):
        """Wipe rainbow across display a pixel at a time."""
        self.current_pattern = "rainbowWipeAlwaysOn"
        self.delay_ms = delay_ms
    
        while True:
            offset = randint(0, 255)
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i,  self.wheel((i+offset) & 255))
                self.strip.show()
                time.sleep(self.delay_ms / 1000.0)
            offset = randint(0, 255)
            for i in range(self.strip.numPixels(), 0, -1):
                self.strip.setPixelColor(i,  self.wheel((i+offset) & 255))
                self.strip.show()
                time.sleep(self.delay_ms / 1000.0)
    

    def randomWipe(self, delay_ms=35):
        """Wipe rainbow across display a pixel at a time."""
        self.current_pattern = "randomWipe"
        self.delay_ms = delay_ms
        while True:
            # for i in range(self.strip.numPixels()):
            #     self.strip.setPixelColor(i, self.wheel((i) & 255))
            #     self.strip.show()
            #     time.sleep(delay_ms / 1000.0)
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i,  self.wheel((i+randint(0, 255)) & 255))
                self.strip.show()
                time.sleep(self.delay_ms / 1000.0)


    def colorShots(self, min=20, length=5, delay_ms_min=10, delay_ms_max=30):
        self.current_pattern = "colorShots"
        while True:
            rand_rgb = self.randomRGB()
            endpoint = randint(min, self.strip.numPixels())
            rand_delay_ms = randint(delay_ms_min, delay_ms_max)
            if randint(0, 1) == 0:
                # go from left
                for i in range(endpoint-length):
                    '''move the segment along the strip'''
                    self.lightSegment(i, i+length, rand_rgb)
                    time.sleep(rand_delay_ms / 1000.0)
                for i in range(length-3):
                    '''fade the segment out'''
                    self.lightSegment(endpoint-length+i, endpoint, rand_rgb)
                    time.sleep(rand_delay_ms / 1000.0)
            else:
                # go from right
                for i in range(self.strip.numPixels(), endpoint+length, -1):
                    '''move the segment along the strip'''
                    self.lightSegment(i-length, i, rand_rgb)
                    time.sleep(rand_delay_ms / 1000.0)
                for i in range(length-3):
                    '''fade the segment out'''
                    self.lightSegment(endpoint, endpoint+length-i, rand_rgb)
                    time.sleep(rand_delay_ms / 1000.0)
            # rand_rgb = [randint(0, 255) for _ in range(3)]
            rand_rgb = self.randomRGB(min_diff=100)
            explosion_size = randint(70, 300)
            explosion_delay_ms = randint(5, 10)
            self.explosion(rand_rgb, endpoint, size=explosion_size, fade=.2, delay_ms=explosion_delay_ms)
            # clear the strip
            self.clear()


    def fireShotLeft(self, min, length, delay_ms_min, delay_ms_max):
        rand_rgb = self.randomRGB()
        endpoint = randint(min, self.strip.numPixels())
        rand_delay_ms = randint(delay_ms_min, delay_ms_max)
        for i in range(endpoint-length):
            '''move the segment along the strip'''
            self.lightSegment(i, i+length, rand_rgb, 
                                exclusive=False, show=False)
            self.strip.setPixelColor(i-1, Color(0, 0, 0))
            self.strip.show()
            time.sleep(rand_delay_ms / 1000.0)
        self.lightSegment(start=endpoint-length-1, end=endpoint, rgb=[0, 0, 0], 
                          exclusive=False, show=True)
        rand_rgb = self.randomRGB(min_diff=100)
        explosion_size = randint(70, 300)
        explosion_delay_ms = randint(5, 10)
        self.explosion(rand_rgb, endpoint, size=explosion_size, fade=.2, delay_ms=explosion_delay_ms)

    def fireShotRight(self, min, length, delay_ms_min, delay_ms_max):
        rand_rgb = self.randomRGB()
        endpoint = randint(min, self.strip.numPixels())
        rand_delay_ms = randint(delay_ms_min, delay_ms_max)
        for i in range(self.strip.numPixels(), endpoint+length, -1):
            '''move the segment along the strip'''
            self.lightSegment(i-length, i, rand_rgb,
                                exclusive=False, show=False)
            self.strip.setPixelColor(i+1, Color(0, 0, 0))
            self.strip.show()
            time.sleep(rand_delay_ms / 1000.0)
        self.lightSegment(endpoint-1, endpoint+length+1, [0, 0, 0],
                          exclusive=False, show=True)
        rand_rgb = self.randomRGB(min_diff=100)
        explosion_size = randint(150, 300)
        explosion_delay_ms = randint(3, 7)
        self.explosion(rand_rgb, endpoint, size=explosion_size, fade=.2, delay_ms=explosion_delay_ms)




    def fireShotRandom(self, min, length, delay_ms_min, delay_ms_max):
        if randint(0, 1) == 0:
            self.fireShotLeft(min, length, delay_ms_min, delay_ms_max)
        else:
            self.fireShotRight(min, length, delay_ms_min, delay_ms_max)

    def colorShotsMultiple(self, min=20, length=5, delay_ms_min=5, delay_ms_max=20):
        self.current_pattern = "colorShotsMultiple"

        while True:
            thread1 = threading.Thread(target=self.fireShotRandom, 
                                       kwargs={"min": min, 
                                               "length": length,
                                                "delay_ms_min": delay_ms_min,
                                                  "delay_ms_max": delay_ms_max})
            thread2 = threading.Thread(target=self.fireShotRandom,
                                       kwargs={"min": min, 
                                               "length": length,
                                                "delay_ms_min": delay_ms_min,
                                                  "delay_ms_max": delay_ms_max})

            thread1.start()
            time.sleep(1)
            thread2.start()
            time.sleep(1)
            thread1.join()
            self.clear()


    def theaterChase(self, rgb, delay_ms=50):
        """Movie theater light style chaser animation."""
        self.current_pattern = "theaterChase"
        self.rgb = rgb
        self.delay_ms = delay_ms
        while True:
            for q in range(3):
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, Color(*self.rgb))
                self.strip.show()
                time.sleep(self.delay_ms / 1000.0)
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, 0)

    
    def rainbowCycle(self, delay_ms=20, iterations=5):
        """Draw rainbow that uniformly distributes itself across all pixels."""
        self.current_pattern = "rainbowCycle"
        self.delay_ms = delay_ms
        while True:
            for j in range(256 * iterations):
                for i in range(self.strip.numPixels()):
                    self.strip.setPixelColor(i, self.wheel((int(i * 256 / self.strip.numPixels()) + j) & 255))
                self.strip.show()
                time.sleep(self.delay_ms / 1000.0)
    

    def theaterChaseRainbow(self, delay_ms=50):
        """Rainbow movie theater light style chaser animation."""
        self.current_pattern = "theaterChaseRainbow"
        self.delay_ms = delay_ms
        while True:
            for j in range(256):
                for q in range(3):
                    for i in range(0, self.strip.numPixels(), 3):
                        self.strip.setPixelColor(i + q, self.wheel((i + j) % 255))
                    self.strip.show()
                    time.sleep(self.delay_ms / 1000.0)
                    for i in range(0, self.strip.numPixels(), 3):
                        self.strip.setPixelColor(i + q, 0)



    def lightSegment(self, start, end, rgb, exclusive=True, show=True):
        '''Light a segment of the strip with a single color. 
        If exclusive is True, turn off all other LEDs.
          If show is True, update the strip.'''
        color = Color(*rgb)
        if exclusive:
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, Color(0, 0, 0))
        for i in range(start, end):
            self.strip.setPixelColor(i, color)
        if show:
            self.strip.show()

    def randomRGB(self, min_diff=80):
        x = [randint(0, 255) for _ in range(3)]
        if np.abs(x[0] -  x[1]) > min_diff or np.abs(x[1] - x[2]) > min_diff or np.abs(x[0] - x[2]) > min_diff:
            return x
        else:
            return self.randomRGB()


    def explosion(self, rgb, center, size=80, fade=0, delay_ms=20):
        '''Create an explosion effect at the center of the strip'''
        # create an array of size size//2 which has evenly spaced numbers from 1.0 to fade
        fade = np.linspace(1.0, fade, size//2)
        for i in range(size//2):
            rgb = [int(c * (fade[i])) for c in rgb]
            if np.mean(rgb) < 10:
                break
            color = Color(*rgb)
            self.strip.setPixelColor(center + i, color)
            self.strip.setPixelColor(center - i, color)
            self.strip.show()
            if i < size//2 - 1:
                time.sleep(delay_ms / 1000.0)
            

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
    
    def rainbow(self, delay_ms=20, iterations=1):
        """Draw rainbow that fades across all pixels at once."""
        while True:
            for j in range(256 * iterations):
                for i in range(self.strip.numPixels()):
                    self.strip.setPixelColor(i, self.wheel((i + j) & 255))
                self.strip.show()
                time.sleep(delay_ms / 1000.0)

    def get_params(self):
        return {"rgb": self.rgb,
                 "delay_ms": self.delay_ms, 
                 "current_pattern": self.current_pattern}
    
    def set_params(self, **kwargs):
        if "rgb" in kwargs:
            self.rgb = kwargs["rgb"]
        if "delay_ms" in kwargs:
            self.delay_ms = kwargs["delay_ms"]
        # if "current_pattern" in kwargs:
        #     self.current_pattern = kwargs["current_pattern"]
        

    def clear(self, show=True):
        self.current_pattern = "clear"
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, Color(0, 0, 0))
        if show:
            self.strip.show()
    

if __name__ == "__main__":
    # create an argparser and add arguments for each of the functions in the LED class
    parser = argparse.ArgumentParser(description="LED strip control")
    parser.add_argument("function", type=str, help="The function to call")
    parser.add_argument("--color", type=str, help="The color to use as comma separated RGB values")
    parser.add_argument("--brightness", type=float, help="The brightness scale", default=1.0)
    args = parser.parse_args()

    led = LED(args.brightness)
    try:
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
            color = [255, 255, 255]
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
        elif args.function == "colorShots":
            # color = [127, 127, 127]
            # if args.color:
            #     color = [int(c) for c in args.color.split(",")]
            led.colorShots()
        elif args.function == "rainbowWipeAlwaysOn":
            led.rainbowWipeAlwaysOn()
        elif args.function == "rainbowWipe":
            led.rainbowWipe()
        elif args.function == "randomWipe":
            led.randomWipe()
        elif args.function == "clear":
            led.clear()
        else:
            print("Invalid function")
            exit(1)
    except KeyboardInterrupt:
        led.clear()
        raise SystemExit