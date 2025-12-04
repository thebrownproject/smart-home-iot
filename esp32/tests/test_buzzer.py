from outputs.buzzer import Buzzer
from outputs.buzzer import BuzzerManager
from tests.TestingSuite import PicoTestBase
import time

class TestBuzzer(PicoTestBase):
    def __init__(self):
        self.buzzer = Buzzer()
    
    def test_start(self):
        print("TestBuzzer: start")
        self.buzzer.start()
        assert self.buzzer.is_running, "Buzzer is not running"
        time.sleep(1)
    
    def test_stop(self):
        print("TestBuzzer: stop")
        self.buzzer.stop()
        assert not self.buzzer.is_running, "Buzzer is still running"
        time.sleep(1)

class testBuzzerManager(PicoTestBase):
    def __init__(self):
        self.buzzer_manager = BuzzerManager()
    
    def test_start(self):
        print("TestBuzzerManager: start")
        self.buzzer_manager.start(1)
        assert self.buzzer_manager.is_running, "Buzzer is not running"
        time.sleep(1)
    
    def test_stop(self):
        print("TestBuzzerManager: stop")
        self.buzzer_manager.stop()
        assert not self.buzzer_manager.is_running, "Buzzer is still running"
        time.sleep(1)
    
    def test_update(self):
        print("TestBuzzerManager: update")
        self.buzzer_manager.start(3)
        self.buzzer_manager.update()
        assert self.buzzer_manager.countdown == 2, "Countdown is not 2"
        time.sleep(1)
        self.buzzer_manager.update()
        assert self.buzzer_manager.countdown == 1, "Countdown is not 1"
        time.sleep(1)
        self.buzzer_manager.update()
        assert self.buzzer_manager.countdown == 0, "Countdown is not 0"
        assert not self.buzzer_manager.is_running, "Buzzer is still running"
        time.sleep(1)