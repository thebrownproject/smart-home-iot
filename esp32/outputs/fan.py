from machine import Pin, PWM

class Fan:
    def __init__(self):
        self.ina = PWM(Pin(19, Pin.OUT), 10000)
        self.inb = PWM(Pin(18, Pin.OUT), 10000)

    def on(self):
        self.ina.duty(0)
        self.inb.duty(700)
    
    def off(self):
        self.ina.duty(0)
        self.inb.duty(0)