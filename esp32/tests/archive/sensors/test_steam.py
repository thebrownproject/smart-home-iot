from sensors.steam import SteamSensor
from tests.TestingSuite import PicoTestBase
import time

class testSteamSensor(PicoTestBase):
    def __init__(self):
        self.steam_sensor = SteamSensor()
    
    def test_is_moisture_detected(self):
        result = self.steam_sensor.is_moisture_detected()
        assert isinstance(result, bool), "Result is not a boolean"
        time.sleep(1)