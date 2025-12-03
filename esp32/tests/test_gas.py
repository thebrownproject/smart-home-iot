from sensors.gas import GasSensor
from tests.TestingSuite import PicoTestBase
import time

class testGasSensor(PicoTestBase):
    def __init__(self):
        self.gas_sensor = GasSensor()
    
    def test_is_gas_detected(self):
        result = self.gas_sensor.is_gas_detected()
        assert isinstance(result, bool), "Result is not a boolean"
        time.sleep(1)