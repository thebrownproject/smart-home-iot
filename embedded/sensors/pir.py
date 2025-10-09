from machine import Pin
import time

class PIRSensor:
    def __init__(self):
        self.pir = Pin(14, Pin.IN)
        self.last_trigger_time = 0
        self.debounce_time = 500
    
    def read(self):
        return self.pir.value()

    def is_motion_detected(self):
        if self.pir.value() == 1:
            now = time.ticks_ms()
            if time.ticks_diff(now, self.last_trigger_time) > self.debounce_time:
                self.last_trigger_time = now
                return True
        return False