from microbit import *
import radio
import math
import random
import machine
import music
import utime

SignalStrength = -60

display.on()
radio.on()
radio.config(length=48)

start_time = running_time()

global colour
colour = 0

receiveColour = 0
receiveState = 0
receiveCount = 0

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

def vibrate():
    pin2.write_digital(1)
    sleep(1000)
    pin2.write_digital(0)
    # print("vibrate code here")

game = 0

if (button_a.is_pressed()):
    colour = 1
    game = 0

if (button_b.is_pressed()):
    colour = 2
    game = 0
    display.show(Image.SKULL)

if (button_a.is_pressed() and button_b.is_pressed() ):
    colour = 0
    game = 1
    display.show(Image.UMBRELLA)
else:
    display.show(Image.SKULL)

def updateState(toMachine, sendColour):
    global game
    message = getHeaderBytes() + getMachine() + "," + toMachine + ",{:d}".format(sendColour)
    # myDebug("send:" + message);
    radio.send(message)

lastID = getMachine()

def signaller():
    global colour
    global wasTogether
    global lastID
    global isAUp
    global isADown
    global isBUp
    global isBDown
    global isTogether
    global wasTogether

    while True:
        # always receive the radio broadcasts
        incoming = radio.receive_full()
        while incoming is not None:
            
            msgbytes, rssi, timestamp = incoming
            
            msg = str(msgbytes)
            
            start = msg.find(getHeaderBytes())
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
                if toMachine == "x":
                    
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
            updateState( "x", 2)
        elif isAUp and (isTogether==0):
            updateState( "x", 0)
        elif isBUp and (isTogether==0): 
            updateState( "x", 1)
            
        # Show a pattern
        if colour == 0:
            display.show(Image.SQUARE)
        if colour == 1:
            display.show(Image.CHESSBOARD)
        if colour == 2:
            display.show(Image.ARROW_N)    
        
def contagion():
    global start_time
    global colour
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

                recvMachineID, toMachine, b = finalmsg.split(',')
                
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
                        
                    # if we receive a happy face treat it as a reset
                    if( receiveColour == 2 ):
                        receiveColour = 0
                    
                    # two's are effectively immune
                    if colour != receiveColour and colour != 2:
                            
                        # you've been saved
                        if receiveColour == 0:
                            colour = receiveColour
                            music.play('C')
                            music.play('B')
                            vibrate()
                                
                        # you've been infected
                        if receiveColour == 1:
                            colour = receiveColour
                            music.play('A')
                            vibrate()
                        
                        # you can't be infected if your colour is 2. You are immune
                            
            incoming = radio.receive_full()

        elapsed_time = running_time() - start_time
        if( elapsed_time > 3000) and ( colour > 0 ):
             start_time = running_time()
             updateState("x",colour)
 
        dot = Image( "00000:"
                     "00000:"
                     "00800:"
                     "00000:"
                     "00000")
        if colour == 0:
            display.show(dot)
        if colour == 1:
            display.show(Image.SQUARE)
        if colour == 2:
            display.show(Image.CHESSBOARD)

# Ensure we can use this to test the micro:bit
music.play('A')
vibrate()
                            
# Update the state so we can log it

# Run contagion
if game == 0:
    contagion()
else:
    updateState( "x", 0)
    signaller()