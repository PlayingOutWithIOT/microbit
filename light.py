# Write your code here :-)
"""
    neopixel_random.py

    Repeatedly displays random colours onto the LED strip.
    This example requires a strip of 8 Neopixels (WS2812) connected to pin0.

"""
from microbit import *
import neopixel
from random import randint

# notes:
# randint(0, 255)

# Setup the Neopixel strip on pin0 with a length of 8 pixels
np = neopixel.NeoPixel(pin0, 24)

display.on()

colour = 0

while True:
    # Iterate over each LED in the strip
    # randint

    if accelerometer.was_gesture("shake"):
        colour = colour + 1
        if colour > 2:
            colour = 0
    
    display.show(colour)
    
    for pixel_id in range(0, len(np)):

        if colour == 0:
            red = 255
            green = 0
            blue = 0

        if colour == 1:
            red = 255
            green = 255
            blue = 0

        if colour == 2:
            red = 0
            green = 255
            blue = 0

        np[pixel_id] = (red, green, blue)

    # Display the current pixel data on the Neopixel strip
    np.show()
       