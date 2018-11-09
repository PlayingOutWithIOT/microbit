# Write your code here :-)
"""
    neopixel_random.py

    Repeatedly displays random colours onto the LED strip.
    This example requires a strip of 8 Neopixels (WS2812) connected to pin0.

"""
from microbit import *
import neopixel
import radio

# notes:
# randint(0, 255)

# Setup the Neopixel strip on pin0 with a length of 8 pixels
np = neopixel.NeoPixel(pin0, 24)

display.on()
radio.on()

colour = 0
count = 0

while True:
    incoming = radio.receive()
    if incoming:   
        a, b = incoming.split(',')
        receiveCount = int(a)
        receiveColour = int(b)
        
        if receiveCount != count:
            count = receiveCount
            colour = receiveColour
            
    if accelerometer.was_gesture("shake"):
        count = count + 1
        colour = colour + 1
            
        if colour > 2:
            colour = 0
            
        message = "{},{}".format(count, colour)
        radio.send(message)
 
    
    display.show(colour)
    
    for pixel_id in range(0, len(np)):

        if colour == 0:
            red = 255
            green = 0
            blue = 0

        if colour == 1:
            red = 128
            green = 255
            blue = 0

        if colour == 2:
            red = 0
            green = 255
            blue = 0
        
        np[pixel_id] = (red, green, blue)
        
    # Display the current pixel data on the Neopixel strip
    np.show()
       