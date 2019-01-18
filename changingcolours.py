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
import machine

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

receiveColour = 0
receiveState = 0
receiveCount = 0

headerBytes = "msg";

def getMachine():
    return "".join("%02x" % i for i in machine.unique_id())

machineID = "".join("%02x" % i for i in machine.unique_id())

print("Machine ID: " + machineID)

def updateState():
    global count
    global colour
    global play
    
    machineID = getMachine()
    
    message = headerBytes + machineID + ",{:d},{:d}".format(count, colour)
    # print("message " + message )
    radio.send(message)

while True:
                
    # always receive the radio broadcasts
    incoming = radio.receive_full()
    while incoming is not None:
        
        msgbytes, rssi, timestamp = incoming
        
        msg = str(msgbytes);
       
        start = msg.find(headerBytes);
        if( start > 0 ):
            finalmsg = msg[start + len(headerBytes):len(msg)-1]
            
            debugRSSI = "{}".format(rssi)
            print("Incoming: " + debugRSSI )
            
            # msg = base64.b64decode(msg).decode('utf-8', 'ignore')
            # print("Msg: " + finalmsg )
            
            a, b, c = finalmsg.split(',')
            
            print("Machine ID: " + a )
            receiveCount = int(b)
            receiveColour = int(c)
           
            # update our values if it's a broadcast we haven't seen
            if receiveCount > count:
                count = receiveCount
                colour = receiveColour
        
        incoming = radio.receive_full()

    elapsed_time = running_time() - start_time
    if elapsed_time > 100:
        start_time = running_time()
        updateState()
        
    if (button_a.was_pressed() | button_b.was_pressed()):
        count = count + 1
        colour = colour + 1
            
        if colour > 2:
            colour = 0
            
        updateState()
    
    display.show(colour)

    for pixel_id in range(0, 24):

        if colour == 0:
            red = 8
            green = 0
            blue = 0

        if colour == 1:
            red = 8
            green = 8
            blue = 0

        if colour == 2:
            red = 0
            green = 8
            blue = 0
        
        np[pixel_id] = (red, green, blue)
        
    # Display the current pixel data on the Neopixel strip
    np.show()