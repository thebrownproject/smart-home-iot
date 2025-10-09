from machine import Pin
import time

class LED:
    def __init__(self):
        self.led = Pin(12, Pin.OUT)
    
    def on(self):
        self.led.value(1)
    
    def off(self):
        self.led.value(0)
    
    def toggle(self):
        self.led.value(not self.led.value())