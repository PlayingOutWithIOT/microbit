from microbit import *
import radio
import math
import random
import machine
import music
import utime

SignalStrength = -90

display.on()
radio.on()

start_time = running_time()

global colour
colour = 0

receiveColour = 0
receiveState = 0
receiveCount = 0

def getHeaderBytes():
    return "msg"
    
def getMachine():
    return "".join("%02x" % i for i in machine.unique_id())

def vibrate():
    print("vibrate code here")

print("Machine ID: " + getMachine() )

if (button_a.was_pressed()):
    colour = 1

if (button_b.was_pressed()):
    colour = 2
        
def updateState():
    global colour
    message = getHeaderBytes() + getMachine() + ",{:d}".format(colour)
    # print(message)
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
    if( elapsed_time > 1000) and ( colour > 0 ):
         start_time = running_time()
         # print( "Updating state");
         updateState()
    
    # if( button_a.was_pressed() and button_b.was_pressed() ):
    #    count = count + 1
    #    colour = 2
    #    updateState()
    
    dot = Image( "00000:"
                 "00000:"
                 "00800:"
                 "00000:"
                 "00000")
    if colour == 0:
        display.show(dot)
    if colour == 1:
        display.show(Image.SAD)
    if colour == 2:
        display.show(Image.HAPPY)
        