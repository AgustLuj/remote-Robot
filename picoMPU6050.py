from imu import MPU6050
import time
from machine import Pin, I2C

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
imu = MPU6050(i2c)
girosc_ang_z_prev=0

startTime = time.ticks_ms()
while True:
    dt = time.ticks_ms()-startTime;
    startTime=time.ticks_ms();
    angleZ= round(imu.gyro.z)-1
    angle = (angleZ)*dt/1000.0 + girosc_ang_z_prev;
    girosc_ang_z_prev = angle
    print(round(angle))
    # Following sleep statement makes values enought stable to be seen and
    # read by a human from shell
