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

receiveColour = 0
receiveState = 0
lastID = 0

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
    message = getHeaderBytes() + getMachine() + ",{:d}".format(colour)
    radio.send(message)

colour = -1
updateState()
colour = 0

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
            serialMsg = recvMachineID + "," + nowStr + "," + debugRSSI + ",{:d}".format(receiveColour)
            print(serialMsg) # if we want to collect what is being sent
                
            # db -47 is close
            # db -100 is 12m
            if (colour != -1 ) and ( lastID != recvMachineID ):
                lastID = recvMachineID
            
                if rssi > SignalStrength:
                    if colour == 0:
                        music.play('A')
                    if colour == 1:
                        music.play('AG')
                    if colour == 2:
                        music.play('CC')
                    colour = receiveColour
                    
                    
        incoming = radio.receive_full()

    isA = button_a.is_pressed()
    isB = button_b.is_pressed()
        
    # ------------------------------------------
    # New algorithmn for detecting button presses
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
        
    if not isA and not isB:
        if isTogether:
            wasTogether = 1
            isTogether = 0
        else:
            wasTogether = 0
    # ------------------------------------------
    
    # were either A or B released?
    if wasTogether:
        colour = 2
        updateState()
    elif isAUp and (isTogether==0):
        colour = 0
        updateState()
    elif isBUp and (isTogether==0):
        colour = 1
        updateState()
        
    # Show a pattern
    if colour == 0:
        display.show(Image.SQUARE)
    if colour == 1:
        display.show(Image.CHESSBOARD)
    if colour == 2:
        display.show(Image.ARROW_N)    