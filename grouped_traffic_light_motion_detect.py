# Write your code here :-)
"""
    neopixel_random.py

    Repeatedly displays random colours onto the LED strip.
    This example requires a strip of 8 Neopixels (WS2812) connected to pin0.

"""
from microbit import *
import neopixel
import radio
import math
import random

print("Starting up Play:bit")

# notes:
# randint(0, 255)

# Setup the Neopixel strip on pin0 with a length of 8 pixels
np = neopixel.NeoPixel(pin0, 24)

display.on()
radio.on()

start_time = running_time()

global colour
colour = 0
global count
count = 0
global play
play = 0
countdown = 24
swirlCount = 0

receiveColour = 0
receiveState = 0
receiveCount = 0

def updateState():
    global count
    global colour
    global play
    message = "{},{},{}".format(count, colour, play)
    radio.send(message)

while True:
                
    # always receive the radio broadcasts
    incoming = radio.receive()
    if incoming:
        print("Incoming")
        a, b, c = incoming.split(',')
        receiveCount = int(a)
        receiveColour = int(b)
        receiveState = int(c)

        # update our values if it's a broadcast we haven't seen
        if receiveCount != count:
            count = receiveCount
            colour = receiveColour
            
    if play == 0:
        x = accelerometer.get_x()
        y = accelerometer.get_y()
        z = accelerometer.get_z()
        mag = math.sqrt(x * x + y * y + z * z)
        # print(mag)
        
        if ((colour == 0) & (mag > 1500)):
            countdown = countdown - 1
        if ((colour == 1) & (mag > 2100)):
            countdown = countdown - 1
        if ((colour == 2) & (mag > 2500)):
            countdown = countdown - 1
        else:
            countdown += 0.1
        
        if countdown > 24:
            countdown = 24
        if countdown < 0:
            countdown = 0
            play = 1
            updateState()
                
        if (button_a.was_pressed() | button_b.was_pressed()):
            count = count + 1
            colour = colour + 1
                
            if colour > 2:
                colour = 0
                
            updateState()
     
        display.show(colour)
        
        for pixel_id in range(0, 24):
            np[pixel_id] = (0, 0, 0)
        
        lights = round(countdown)
        for pixel_id in range(0, lights):

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
    else:
        if play == 1:
            
            display.show("X")
    
            red = random.randrange(0, 255)
            green = random.randrange(0, 255)
            blue = random.randrange(0, 255)
            
            # your code
            elapsed_time = running_time() - start_time
            if elapsed_time > 300:
                start_time = running_time()
                swirlCount = swirlCount + 1

            for pixel_id in range(0, 24):
                np[pixel_id] = (0, 0, 0)
                
            for pixel_id in range(0, 8):
                np[(pixel_id + swirlCount + 0) % 24] = (255, 0, 0)
                np[(pixel_id + swirlCount + 8) % 24] = (128, 255, 0)
                np[(pixel_id + swirlCount + 16) % 24] = (0, 255, 255)
            np.show()

