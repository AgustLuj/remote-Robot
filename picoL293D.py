from machine import Pin, PWM, I2C
from time import sleep,ticks_ms
from imu import MPU6050

M1pwmPIN=16
M2pwmPIN=17
M1cwPin=14 
M1acwPin=15
M2cwPin=10
M2acwPin=11

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
imu = MPU6050(i2c)
girosc_ang_z_prev=0

startTime = ticks_ms();

def convertAndSetAngle():
    global girosc_ang_z_prev;
    global startTime;
    dt = ticks_ms()-startTime;
    startTime=ticks_ms();
    angleZ= round(imu.gyro.z)-1
    angle = (angleZ)*dt/1000.0 + girosc_ang_z_prev;
    girosc_ang_z_prev = angle
    print(round(angle))

class Motor():
    def __init__(self,cwGP,acwGP,speedGP):
        self.cw = Pin(cwGP, Pin.OUT)
        self.acw = Pin(acwGP, Pin.OUT)
        self.Speed = PWM(Pin(speedGP))
    def moveStop(self):
        self.cw.value(0)
        self.acw.value(0)
    def moveForward(self):
        self.cw.value(1)
        self.acw.value(0)
    def moveBack(self):
        self.cw.value(0)
        self.acw.value(1)
    def setSpeed(self,speed):
        self.Speed.freq(50)
        self.Speed.duty_u16(int(speed/100*65536))

def motorMove(speed,direction):
    Motor1 = Motor(M1cwPin,M1acwPin,M1pwmPIN);
    Motor2 = Motor(M2cwPin,M2acwPin,M2pwmPIN);
    
    Motor1.setSpeed(speed)
    Motor2.setSpeed(speed)
    if direction == 0:
        Motor1.moveStop();
        Motor2.moveStop();
    if direction == 1:
        Motor1.moveForward();
        Motor2.moveForward();
    if direction == 2:
        Motor1.moveBack();
        Motor2.moveBack();
    if direction == 3:
        Motor1.moveStop();
        Motor2.moveForward();
    if direction == 4:
        Motor1.moveForward();
        Motor2.moveStop();
    
# main program
motorMove(100,0);
while True:
    convertAndSetAngle()
    if girosc_ang_z_prev <= 5 and girosc_ang_z_prev >= -5:
        print('stop')
        motorMove(100,0);
    if girosc_ang_z_prev >= 6 and girosc_ang_z_prev <= 90:
        print('derecha')
        motorMove(50,4);
    if girosc_ang_z_prev <= -6 and girosc_ang_z_prev >= -360:
        print('izquierda')
        motorMove(50,3);
