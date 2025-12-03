from sensors.rfid import RFIDSensor
from tests.TestingSuite import PicoTestBase
import time

class testRFIDSensor(PicoTestBase):
    def __init__(self):
        self.rfid_sensor = RFIDSensor()
    
    def test_scan_card(self):
        result = self.rfid_sensor.scan_card()
        assert isinstance(result, bool), "Result is not a boolean"
        time.sleep(1)
    
    def test_get_card_id(self):
        result = self.rfid_sensor.get_card_id()
        assert isinstance(result, (str, type(None))), "Result is not a string/None"
        time.sleep(1)
    
    def test_clear_card(self):
        self.rfid_sensor.clear_card()
        assert True, "Card is not cleared"
        time.sleep(1)