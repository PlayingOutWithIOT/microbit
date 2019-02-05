from microbit import *
import radio
import math
import random
import machine
import music
import utime

# print("Starting up Play:bit")

display.on()
radio.on()

start_time = running_time()

SignalStrength = -70

global colour
colour = 0
global count
count = 0

receiveColour = 0
receiveState = 0
receiveCount = 0

def getHeaderBytes():
    return "msg"
    
def getMachine():
    return "".join("%02x" % i for i in machine.unique_id())

machineID = "".join("%02x" % i for i in machine.unique_id())

print("Machine ID: " + getMachine() )

def updateState():
    global count
    global colour
    message = getHeaderBytes() + getMachine() + ",{:d},{:d}".format(count, colour)
    radio.send(message)

while True:
                
    # always receive the radio broadcasts
    incoming = radio.receive_full()
    while incoming is not None:
        
        msgbytes, rssi, timestamp = incoming
        
        msg = str(msgbytes);
       
        start = msg.find(getHeaderBytes());
        if( start > 0 ):
            finalmsg = msg[start + len(getHeaderBytes()):len(msg)-1]
            
            debugRSSI = "{}".format(rssi)

            recvMachineID, b, c = finalmsg.split(',')
            
            # print("Machine ID: " + a )
            receiveCount = int(b)
            receiveColour = int(c)
           
            # update our values if it's a broadcast we haven't seen
            if receiveCount > count:
                
                # get the date time
                now = utime.ticks_ms()
                nowStr = str(now)
                
                # construct the serial message
                serialMsg = recvMachineID + "," + nowStr + "," + debugRSSI + ",{:d},{:d}".format(count, colour)
                print(serialMsg) # if we want to collect what is being sent
                
                # db -47 is close
                # db -100 is 12m 
                if rssi > SignalStrength:
                    music.play('A')
                    colour = receiveColour
                
                count = receiveCount
                    
        incoming = radio.receive_full()

    # elapsed_time = running_time() - start_time
    # if elapsed_time > 100:
    #     start_time = running_time()
    #     updateState()
        
    if (button_a.was_pressed() | button_b.was_pressed()):
        count = count + 1
        colour = colour + 1

        if colour > 1:
            colour = 0
            
        updateState()
    
    if colour == 0:
        display.show(Image.HAPPY)
    if colour == 1:
        display.show(Image.SAD)
        