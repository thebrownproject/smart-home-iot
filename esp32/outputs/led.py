from machine import Pin

class LED:
    def __init__(self):
        self.led = Pin(12, Pin.OUT)
    
    def on(self):
        self.led.value(1)
    
    def off(self):
        self.led.value(0)