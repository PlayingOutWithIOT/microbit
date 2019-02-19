from microbit import *
import radio
import math
import random
import machine
import music
import utime
import time

# print("Starting up Play:bit")

display.on()
radio.on()
radio.config(length=48)

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
    return "msg:"
    
def getNullMachine():
    return "x"
    
def getMachine():
    return "".join("%02x" % i for i in machine.unique_id())

def updateState(toMachine, sendColour):
    message = getHeaderBytes() + getMachine() + "," + toMachine + ",{:d}".format(sendColour)
    # myDebug("send:" + message);
    radio.send(message)
    
def myDebug(message):
    test = 0
    # print(message)
    
machineID = "".join("%02x" % i for i in machine.unique_id())

myDebug("Machine ID: " + getMachine() )

updateState( getMachine(), -1 )      # send to yourself
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
            # print("recv:" + finalmsg)
             
            debugRSSI = "{}".format(rssi)

            recvMachineID, toMachine, b = finalmsg.split(',')
            
            # print("Machine ID: " + a )
            receiveColour = int(b)
            
            # get the date time
            now = utime.ticks_ms()
            nowStr = str(now)
                
            # construct the serial message
            serialMsg = recvMachineID + "," + nowStr + "," + debugRSSI + ",{:d}".format(receiveColour)
            print(serialMsg)
                
            # We are forcing the colour to set as an ACK
            if toMachine == getNullMachine():
                myDebug("received broadcast: " + serialMsg)
                
                # Otherwise we need to make a choice to whether we set our colour 
                if( lastID != recvMachineID ):
                    lastID = recvMachineID
                    
                    # db -47 is close
                    # db -100 is 12m
                    if rssi > SignalStrength:
                        colour = receiveColour
                        updateState(recvMachineID,colour)    # Send the ACK
                        if colour == 0:
                            music.play('A')
                        if colour == 1:
                            pin2.write_digital(1)
                            sleep(1000)
                            pin2.write_digital(0)
                        if colour == 2:
                            music.play('AG')
            else:
                if toMachine == getMachine():
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

    # Send a new colour according to whether A or B released, A was released or B was released
    if wasTogether:
        updateState( getNullMachine(), 2)
    elif isAUp and (isTogether==0):
        updateState( getNullMachine(), 0)
    elif isBUp and (isTogether==0): 
        updateState( getNullMachine(), 1)
        
    # Show a pattern
    if colour == 0:
        display.show(Image.SQUARE)
    if colour == 1:
        display.show(Image.CHESSBOARD)
    if colour == 2:
        display.show(Image.ARROW_N)    