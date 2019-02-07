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

receiveColour = 0
receiveState = 0

isAUp = 1
isADown = 0
isBUp = 1
isBDown = 0
isTogether = 0
wasTogether = 0

def getHeaderBytes():
    return "msg"
    
def getMachine():
    return "".join("%02x" % i for i in machine.unique_id())

machineID = "".join("%02x" % i for i in machine.unique_id())

print("Machine ID: " + getMachine() )

def updateState():
    global colour
    message = getHeaderBytes() + getMachine() + ",{:d}".format(colour)
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

            recvMachineID, b = finalmsg.split(',')
            
            # print("Machine ID: " + a )
            receiveColour = int(b)

            # get the date time
            now = utime.ticks_ms()
            nowStr = str(now)
                
            # construct the serial message
            serialMsg = recvMachineID + "," + nowStr + "," + debugRSSI + ",{:d}".format(colour)
            print(serialMsg) # if we want to collect what is being sent
                
            # db -47 is close
            # db -100 is 12m 
            if rssi > SignalStrength:
                music.play('A')
                colour = receiveColour
                    
        incoming = radio.receive_full()

    isA = button_a.is_pressed()
    isB = button_b.is_pressed()
        
    # ------------------------------------------
    # New algorithmn for detecting button presses
    if not isA and not isB:
        if isTogether:
            wasTogether = 1
            isTogether = 0
        else:
            wasTogether = 0

    isAUp = 0
    isBUp = 0
    
    # Are either A or B held?
    if isA:
        isAUp = 0
        isADown = 1
    if isB:
        isBUp = 0
        isBDown = 1

    # Were they released?
    if ((not isA) and isADown):
        isAUp = 1
        isADown = 0
    if ((not isB) and isBDown):
        isBUp = 1
        isBDown = 0
    if isA and isB:
        isTogether = 1
    # ------------------------------------------
    
    # were either A or B released?
    if isAUp and (isTogether==0):
        colour = 0
        updateState()
    if isBUp and (isTogether==0):
        colour = 1
        updateState()
    if wasTogether:
        colour = 2
        updateState()
        
    # Show a pattern
    if colour == 0:
        display.show(Image.HAPPY)
    if colour == 1:
        display.show(Image.SAD)
    if colour == 2:
        display.show(Image.SURPRISED)    