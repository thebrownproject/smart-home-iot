from machine import Pin

class LED:
    def __init__(self):
        self._led = Pin(12, Pin.OUT)
        self._is_on = None
    
    def on(self):
        self._led.value(1)
        self._is_on = True
    
    def off(self):
        self._led.value(0)
        self._is_on = False

    def is_on(self):
        return self._is_on