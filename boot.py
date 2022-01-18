try:
  import usocket as socket
except:
  import socket

from machine import Pin
import network

import esp
esp.osdebug(None)

import gc
gc.collect()

ssid = 'esp32_baum'
password = 'Baum12345'

ap = network.WLAN(network.AP_IF)
ap.config(essid=ssid, authmode=network.AUTH_WPA_WPA2_PSK, password = password)
ap.active(True)
print(ap.ifconfig())


led_rot = Pin(15, Pin.OUT)
led_gruen = Pin(17, Pin.OUT)

