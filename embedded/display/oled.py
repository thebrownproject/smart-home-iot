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
