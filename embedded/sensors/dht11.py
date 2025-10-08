# Import machine, time and dht modules. 
import machine
import time
import dht
from time import sleep_ms, ticks_ms 
from machine import Pin 

#Associate DHT11 with Pin(17).
class DHT11Sensor:
    def __init__(self, pin_number=17):
        self.dht = dht.DHT11(machine.Pin(pin_number))
    
    def read_data(self):
        try:
            self.dht.measure()
            return self.dht.temperature(), self.dht.humidity()
        except OSError as e:
            print(f"DHT11 read error: {e}")
            return None, None
    
    def read_temperature(self):
        try:
            self.dht.measure()
            return self.dht.temperature()
        except OSError as e:
            print(f"DHT11 read error: {e}")
            return None

    def read_humidity(self):
        try:
            self.dht.measure()
            return self.dht.humidity()
        except OSError as e:
            print(f"DHT11 read error: {e}")
            return None