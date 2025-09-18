from machine import SoftI2C, Pin 
from i2c_lcd import I2cLcd 

class DisplayManager:
    def __init__(self):
        self.i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000)
        self.lcd = I2cLcd(self.i2c, 0x27, 2, 16)

    def display_data(self, temperature, humidity):
        self.lcd.move_to(0, 0)
        self.lcd.putstr(f"Temp: {temperature}°C")
        self.lcd.move_to(0, 1)
        self.lcd.putstr(f"Hum: {humidity}%")
    
    def clear_display(self):
        self.lcd.clear()
    
    def display_text(self, text):
        self.lcd.putstr(text)

# Test the DisplayManager class
display_manager = DisplayManager()
display_manager.display_text("Hello, World1")