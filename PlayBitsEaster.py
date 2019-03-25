from microbit import *

# MPR121 Capacitive Touch (init/reset/touch) based on
# http://www.multiwingspan.co.uk/micro.php?page=mpr121

class mpr121:
    
    def __init__(self):
        self.ADDRESS = 0x5a
        self.TOUCHTH_0 = 0x41
        self.RELEASETH_0 = 0x42
        self.SOFTRESET = 0x80
        self.ECR = 0x5E
        self.MHDR = 0x2B
        self.NHDR = 0x2C
        self.NCLR = 0x2D
        self.FDLR = 0x2E
        self.MHDF = 0x2F
        self.NHDF = 0x30
        self.NCLF = 0x31
        self.FDLF = 0x32
        self.NHDT = 0x33
        self.NCLT = 0x34
        self.FDLT = 0x35
        self.DEBOUNCE = 0x5B
        self.CONFIG1 = 0x5C
        self.CONFIG2 = 0x5D

    def write_reg(self, reg, value):
        i2c.write(self.ADDRESS, bytes([reg, value]), repeat=False)
    
    def touched(self):
        self.write_reg(0, 0)
        lower = i2c.read(self.ADDRESS, 2, repeat=False)        
        return lower[0] + (lower[1] << 8)
        
    # reset of the device    
    def resetBoard(self):
        self.write_reg(self.SOFTRESET, 0x63)
        sleep(1)
        self.write_reg(self.ECR, 0x00)
        # self.set_thresholds(20, 15)
        self.set_thresholds(44, 30)
        self.write_reg(self.MHDR, 0x01)
        self.write_reg(self.NHDR, 0x01)
        self.write_reg(self.NCLR, 0x0E)
        self.write_reg(self.FDLR, 0x00)
        self.write_reg(self.MHDF, 0x01)
        self.write_reg(self.NHDF, 0x05)
        self.write_reg(self.NCLF, 0x01)
        self.write_reg(self.FDLF, 0x00)
        self.write_reg(self.NHDT, 0x00)
        self.write_reg(self.NCLT, 0x00)
        self.write_reg(self.FDLT, 0x00)
        self.write_reg(self.DEBOUNCE, 0x00)
        self.write_reg(self.CONFIG1, 0x10)
        self.write_reg(self.CONFIG2, 0x20)
        self.write_reg(self.ECR, 0x8f)

    def set_thresholds(self, touch, release):
        for i in range(12):
            self.write_reg(self.TOUCHTH_0 + 2*i, touch)
            self.write_reg(self.RELEASETH_0 + 2*i, release)

def set_servo_angle(pin, angle):
    duty = 26 + (angle * 102) / 180
    pin.write_analog(duty)

cap = mpr121()
cap.resetBoard()
last = 0
while True:
    
    # Was a button pressed
    # If so, move the servo
    if button_a.is_pressed():
        angle = 90
        set_servo_angle(pin1, angle)

    if button_b.is_pressed():
        angle = 0
        set_servo_angle(pin1, angle)

    # Was the board touched?
    n = cap.touched()
    if n != last:
        display.clear()
        # look at all pins from 0 to 12 inclusive.
        for pin in range(0, 13):
            if n & (1 << pin):
                # this code is triggered when a certain pin is touched
                # e.g. if you want to repsond to pin 5 use the code
                
                if pin == 0:
                    angle = 0
                    set_servo_angle(pin1, angle)
        
                # Row (x) is pin number modulus 5
                x = pin % 5
                # Column (y) is (int)(pin number divided by 5)                
                y = pin // 5
                
                # Set the repsective LED on the micro:bit                
                display.set_pixel(x, y, 9)   
        last = n