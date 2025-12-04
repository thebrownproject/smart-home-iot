from machine import Pin

class GasSensor:
    def __init__(self):
        self.gas = Pin(23, Pin.IN, Pin.PULL_UP)
    
    def is_gas_detected(self):
        if self.gas.value() == 0:
            return True
        return False