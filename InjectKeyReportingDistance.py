import time
import serial
import serial.tools.list_ports as port_list
import win32api
import time
import win32con
    
# find the port
ports = list(port_list.comports())
for p in ports:
    try:
        portStr = str(p)
        port = portStr[0:5]
        print(port)
        print( "Opening port: " + port )
        ser = serial.Serial( port, 115200, timeout=0)
        break
    except serial.SerialException:
        a = 0

line = ""
while True:
    res = ser.readline()
    if len(res) > 0:
        line = line + res.decode("utf-8")
        line = line.rstrip()
           
        if len(line) == 1:            
            distance = ord(line[0:1])
            
            win32api.keybd_event(distance, 0, 0, 0)            

            win32api.keybd_event(distance, 0, win32con.KEYEVENTF_KEYUP ,0)
            line = ""
