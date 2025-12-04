from sensors.dht11 import DHT11Sensor
from tests.TestingSuite import PicoTestBase
import time

class testDHT11Sensor(PicoTestBase):
    def __init__(self):
        self.dht11_sensor = DHT11Sensor()
    
    def test_read_data(self):
        print("TestDHT11Sensor: read_data")
        result = self.dht11_sensor.read_data()
        assert isinstance(result, tuple), "Result is not a tuple"
        assert len(result) == 2, "Result is not a tuple of length 2"
        assert isinstance(result[0], (int, type(None))), "Temperature is not int/None"
        assert isinstance(result[1], (int, type(None))), "Humidity is not int/None"
        time.sleep(1)