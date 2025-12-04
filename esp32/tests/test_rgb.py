from outputs.rgb import RGB
from outputs.rgb import RGBManager
from tests.TestingSuite import PicoTestBase
import time

class testRGB(PicoTestBase):
    def __init__(self):
        self.rgb = RGB()
    
    def test_set_color(self):
        print("TestRGB: set_color")
        self.rgb.set_color(255, 0, 0)
        assert self.rgb.color == (255, 0, 0), "RGB is not set to red"
        time.sleep(1)
    
    def test_off(self):
        print("TestRGB: off")
        self.rgb.off()
        assert self.rgb.color == (0, 0, 0), "RGB is not off"
        time.sleep(1)
        
class testRGBManager(PicoTestBase):
    def __init__(self):
        self.rgb_manager = RGBManager()

    def test_show(self):
        print("TestRGBManager: show")
        assert self.rgb_manager.show('gas', (255, 0, 0), 1) == True, "Manager is not working"
        time.sleep(1)
    
    def test_update(self):
        print("TestRGBManager: update")
        self.rgb_manager.show('gas', (255, 0, 0), 1)
        self.rgb_manager.update()
        assert self.rgb_manager.countdown == 0, "Countdown is not 0"
        time.sleep(1)
