from outputs.buzzer import Buzzer
from outputs.buzzer import BuzzerManager
from tests.TestingSuite import PicoTestBase
import time

class TestBuzzer(PicoTestBase):
    def __init__(self):
        self.buzzer = Buzzer()
    
    def test_start(self):
        self.buzzer.start()
        assert self.buzzer.is_running(), "Buzzer is not running"
        time.sleep(1)
    
    def test_stop(self):
        self.buzzer.stop()
        assert not self.buzzer.is_running(), "Buzzer is still running"
        time.sleep(1)

class testBuzzerManager(PicoTestBase):
    def __init__(self):
        self.buzzer_manager = BuzzerManager()
    
    def test_start(self):
        self.buzzer_manager.start(1)
        assert self.buzzer_manager.is_running(), "Buzzer is not running"
        time.sleep(1)
    
    def test_stop(self):
        self.buzzer_manager.stop()
        assert not self.buzzer_manager.is_running(), "Buzzer is still running"
        time.sleep(1)