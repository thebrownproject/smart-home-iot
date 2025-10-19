# Import machine, time and dht modules. 
import machine
import time
import dht
from time import sleep_ms, ticks_ms 
from machine import Pin 

class DHT11Sensor:
    def __init__(self):
        self.dht = dht.DHT11(machine.Pin(17))
    
    def read_data(self):
        try:
            self.dht.measure()
            return self.dht.temperature(), self.dht.humidity()
        except OSError as e:
            print(f"DHT11 read error: {e}")
            return None, None