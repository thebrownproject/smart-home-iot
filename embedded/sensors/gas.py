from machine import Pin
import time

class GasSensor:
    def __init__(self):
        self.gas = Pin(23, Pin.IN, Pin.PULL_UP)

    def read_value(self):
        return self.gas.value()
    
    def is_gas_detected(self):
        if self.gas.value() == 0:
            return True
        return False