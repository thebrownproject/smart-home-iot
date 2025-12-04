from machine import Pin, ADC

class SteamSensor:
    def __init__(self):
        self.adc = ADC(Pin(34))
        self.adc.atten(ADC.ATTN_11DB)
        self.adc.width(ADC.WIDTH_12BIT)
    
    def is_moisture_detected(self):
        if self.adc.read() > 746:
            return True
        return False