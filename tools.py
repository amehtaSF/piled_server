
from rpi_ws281x import Color
from random import randint
import numpy as np
import time



def light_segment(strip, left_bound, right_bound, rgb, show=True):
    '''
    Light a segment of the strip with a single color. 

    Parameters:
    strip: NeoPixel instance
    start: int
        The index of the left most pixel of the segment
    end: int
        The index of the right most pixel of the segment
    
    '''
    color = Color(*rgb)
    for i in range(left_bound, right_bound):
        strip.setPixelColor(i, color)
    if show:
        strip.show()

def moving_segment(strip, rgb, lb_start, lb_end, length, step_size, delay_ms):
    '''
    Light a segment of the strip with a single color and move it along the strip.

    Parameters:
    strip: NeoPixel instance
    lb_start: int
        The starting index of the left most pixel of the segment
    lb_end: int
        The ending index of the left most pixel of the segment
    length: int
        The length of the segment
    rgb: tuple
        The RGB color of the segment
    delay_ms: int
        The delay in milliseconds between each movement
    '''
    rgb = threshold_brightness(strip, rgb)

    if lb_start > lb_end:
        step = step_size * -1
    else:
        step = step_size * 1

    prev_i = lb_start
    for i in range(lb_start, lb_end - length, step):
        light_segment(strip, prev_i, prev_i + length, (0, 0, 0), show=False)
        light_segment(strip, i, i + length, rgb, show=True)
        prev_i = i
        time.sleep(delay_ms / 1000.0)


def randomRGB(min_diff=80):
    '''Generate a random RGB color with a minimum difference of min_diff between the channels using rejection sampling.'''
    x = [randint(0, 255) for _ in range(3)]
    if np.abs(x[0] -  x[1]) > min_diff or np.abs(x[1] - x[2]) > min_diff or np.abs(x[0] - x[2]) > min_diff:
        return x
    else:
        return randomRGB()


def explosion(strip, rgb: tuple, center, size=80, fade=0, delay_ms=20):
    '''Create an explosion effect
    
    Parameters:
    strip: NeoPixel instance
    rgb: tuple
        The RGB color of the explosion
    center: int
        The index of the center of the explosion
    size: int
        The size of the explosion
    fade: int
        The amount of fading of the explosion. Int between 0 and 1.
        The lower the value, the less bright, the explosion will be as it moves away from the center.
    delay_ms: int
        The delay in milliseconds between each iteration
    '''
    assert fade >= 0 and fade <= 1, "Fade must be between 0 and 1"
    fade = np.linspace(1.0, fade, size//2)
    for i in range(size//2):
        rgb = [int(c * (fade[i])) for c in rgb]
        if np.mean(rgb) < 10:
            break
        color = Color(*rgb)
        strip.setPixelColor(center + i, color)
        strip.setPixelColor(center - i, color)
        strip.show()
        if i < size//2 - 1:
            time.sleep(delay_ms / 1000.0)
        

def wheel(pos):
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
    

def getMeanBrightness(strip):
    '''Get the mean brightness of the strip'''
    return np.mean([strip.getPixelColor(i) for i in range(strip.numPixels())])


def threshold_brightness(strip, rgb, threshold=127):
    # Calculate the total brightness of the RGB tuple
    mean_brightness = getMeanBrightness(strip)

    # Check if total brightness exceeds the threshold
    if mean_brightness > threshold:
        # Calculate the scaling factor to dampen brightness
        scale_factor = threshold / mean_brightness

        # Dampen the brightness of each component proportionally
        dampened_rgb = tuple(int(value * scale_factor) for value in rgb)
        return dampened_rgb
    else:
        return rgb    
