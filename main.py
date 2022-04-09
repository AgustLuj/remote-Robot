from machine import Pin, Timer
import time
trig = Pin(17, Pin.OUT)
echo = Pin(16, Pin.IN, Pin.PULL_DOWN)

led = Pin(25, Pin.OUT)
timer = Timer()

def blink(timer):
     led.toggle()

timer.init(freq=2.5, mode=Timer.PERIODIC, callback=blink)