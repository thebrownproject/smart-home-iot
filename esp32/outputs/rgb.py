from machine import Pin
import neopixel
import time

class RGB:
    def __init__(self):
        self.pin = Pin(26, Pin.OUT)
        self.np = neopixel.NeoPixel(self.pin, 4)
    
    def set_color(self, r, g, b):
        self.np.fill((r, g, b))
        self.np.write()

    def off(self):
        self.np.fill((0, 0, 0))
        self.np.write()