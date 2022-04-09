from machine import UART, Pin

import time

from esp8266 import ESP8266

esp01 = ESP8266()

esp8266_at_ver = None

led=Pin(25,Pin.OUT)

print("StartUP",esp01.startUP())

#print("ReStart",esp01.reStart())

print("StartUP",esp01.startUP())

print("Echo-Off",esp01.echoING())

print("\r\n\r\n")


esp8266_at_var = esp01.getVersion()

if(esp8266_at_var != None):

    print(esp8266_at_var)

esp01.setCurrentWiFiMode()

print("\r\n\r\n")

print("Try to connect with the WiFi..")

while (1):

    if "WIFI CONNECTED" in esp01.connectWiFi("FMMA","PE20Tj58"):

        print("ESP8266 connect with the WiFi..")

        break;

    else:

        print(".")

        time.sleep(2)

print("\r\n\r\n")

print("Now it's time to start HTTP Get/Post Operation.......\r\n");