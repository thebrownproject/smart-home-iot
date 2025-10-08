from machine import Pin, ADC
import time

class SteamSensor:
    def __init__(self, pin_number=34):
        self.adc = ADC(Pin(pin_number))
        self.adc.atten(ADC.ATTN_11DB)
        self.adc.width(ADC.WIDTH_12BIT)
    
    def read(self):
        return self.adc.read()
    
    def is_moisture_detected(self):
        if self.adc.read() > 746:
            return True
        return False