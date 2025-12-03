from outputs.oled import OLED
from outputs.oled import OLEDManager
from tests.TestingSuite import PicoTestBase
import time

class testOLED(PicoTestBase):
    def __init__(self):
        self.oled = OLED()
    
    def test_show_text(self):
        print("TestOLED: show_text")
        result = self.oled.show_text("Hello", "World!")
        assert result == True, "OLED is not showing text"
        time.sleep(1)

    def test_clear(self):
        print("TestOLED: clear")
        result = self.oled.clear()
        assert result == True, "OLED is not clearing"
        time.sleep(1)

class testOLEDManager(PicoTestBase):
    def __init__(self):
        self.oled_manager = OLEDManager()
    
    def test_show(self):
        print("TestOLEDManager: show")
        assert self.oled_manager.show('gas', "Hello", 1) == True, "Manager is not showing text"
        time.sleep(1)
    
    def test_update(self):
        print("TestOLEDManager: update")
        self.oled_manager.show('gas', "Hello", 3)
        self.oled_manager.update()
        assert self.oled_manager.countdown == 2, "Countdown is not 2"
        time.sleep(1)
        self.oled_manager.update()
        assert self.oled_manager.countdown == 1, "Countdown is not 1"
        time.sleep(1)
        self.oled_manager.update()
        assert self.oled_manager.countdown == 0, "Countdown is not 0"
        assert self.oled_manager.owner == None, "Owner is not None"
        time.sleep(1)