from microbit import *
import radio
import math
import machine
import utime

signalStrength = 0

radio.on()
radio.config(length=48)

# Up
# Down
# Left
# Right
# Space
# A
# S
# D
# W

def getMachine():
    mac_addr = "".join("%02x" % i for i in machine.unique_id())
    return mac_addr

this_machine = getMachine()

print(getMachine() + "." + ".")

display.show(Image.SQUARE)

start_time = running_time()

signals = {}

while True:
        # we only receive a radio broadcast from others
        incoming = radio.receive_full()
        while incoming is not None:
            msg, rssi, timestamp = incoming
            
            signalStrength = rssi
            
            if msg is not None:
                R = " "
                if rssi > -70:
                    R = "A"
                if rssi > -65:
                    R = "S"
                if rssi > -55:
                    R = "D"
                if rssi > -40:
                    R = "W"
                    
                print( R )
                
            incoming = radio.receive_full()
                
        # Send out a distance ping
        elapsed_time = running_time() - start_time
        if elapsed_time > 300:
            start_time = running_time()
            radio.send("blank")
             