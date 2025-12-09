from machine import Pin, PWM

class Fan:
    def __init__(self):
        self._ina = PWM(Pin(19, Pin.OUT), 10000)
        self._inb = PWM(Pin(18, Pin.OUT), 10000)
        self._is_on = None

    def on(self):
        self._ina.duty(0)
        self._inb.duty(700)
        self._is_on = True

    def off(self):
        self._ina.duty(0)
        self._inb.duty(0)
        self._is_on = False

    def is_on(self):
        return self._is_on

class FanManager:
    def __init__(self):
        self.fan = Fan()
        self.is_on = False 
    
    def on(self):
        self.fan.on()
        self.is_on = True

    def off(self):
        self.fan.off()
        self.is_on = False
    
    def update(self):
        pass