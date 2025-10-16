from machine import SoftI2C, Pin
from i2c_lcd import I2cLcd

class OLED:
    def __init__(self):
        self.i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000)
        self.lcd = I2cLcd(self.i2c, 0x27, 2, 16)

    def show_text(self, line1, line2=""):
        self.lcd.clear()
        self.lcd.move_to(0, 0)
        self.lcd.putstr(line1[:16])
        if line2:
            self.lcd.move_to(0, 1)
            self.lcd.putstr(line2[:16])

    def clear(self):
        self.lcd.clear()

    def show_temp_humidity(self, temp, humidity):
        self.lcd.clear()
        self.lcd.move_to(0, 0)
        self.lcd.putstr(f"Temp: {temp}C"[:16])
        self.lcd.move_to(0, 1)
        self.lcd.putstr(f"Humid: {humidity}%"[:16])


class OLEDManager:
    def __init__(self):
        self.oled = OLED()
        self.owner = None
        self.countdown = 0
        self.priority = {'gas': 4, 'rfid': 3, 'steam': 2, 'motion': 1, 'environment': 0}

    def show(self, owner, line1, duration, line2=""):
        """Show text for duration seconds (if priority allows).

        Args:
            owner: Handler name ('gas', 'rfid', 'steam', 'motion', 'environment')
            line1: First line of text (max 16 chars)
            duration: Seconds to display
            line2: Optional second line of text (max 16 chars)
        """
        # Block if current owner has higher priority (higher number = higher priority)
        if self.owner and self.priority[owner] < self.priority[self.owner]:
            return False

        # Grant control
        self.owner = owner
        self.countdown = duration
        self.oled.show_text(line1, line2)
        return True
    
    def update(self):
        """ Call every loop iteration - counts down and turns off when timer expires."""
        if self.countdown > 0:
            self.countdown -= 1
            if self.countdown == 0:
                self.oled.clear()
                self.owner = None