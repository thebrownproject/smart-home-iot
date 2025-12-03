from sensors.pir import PIRSensor
from tests.TestingSuite import PicoTestBase
import time

class testPIRSensor(PicoTestBase):
    def __init__(self):
        self.pir_sensor = PIRSensor()
    
    def test_is_motion_detected(self):
        print("TestPIRSensor: is_motion_detected")
        result = self.pir_sensor.is_motion_detected()
        assert isinstance(result, bool), "Result is not a boolean"
        time.sleep(1)