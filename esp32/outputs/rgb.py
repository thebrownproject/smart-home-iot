from machine import Pin
import neopixel

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

class RGBManager:
    """Manages RGB with priority and countdown timers (no time module needed)."""

    def __init__(self):
        self.rgb = RGB()
        self.owner = None
        self.countdown = 0
        self.priority = {'gas': 3, 'rfid': 2, 'steam': 1, 'motion': 0}

    def show(self, owner, color, duration):
        # Check priority - deny if lower/equal priority is already active
        if self.owner and self.priority[owner] <= self.priority[self.owner]:
            return False
        # Grant control
        self.owner = owner
        self.countdown = duration
        self.rgb.set_color(*color)
        return True

    def update(self):
        if self.countdown > 0:
            self.countdown -= 1
            if self.countdown == 0:
                self.rgb.off()
                self.owner = None