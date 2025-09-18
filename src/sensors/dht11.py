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
        self.dht.measure()
        return self.dht.temperature(), self.dht.humidity()
    
    def get_temperature(self):
        self.dht.measure()
        return self.dht.temperature()
    
    def get_humidity(self):
        self.dht.measure()
        return self.dht.humidity()

# Test the DHT11Sensor class
sensor = DHT11Sensor()
print(sensor.read_data())
print(sensor.get_temperature())
print(sensor.get_humidity())