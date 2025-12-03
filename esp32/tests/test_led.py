from outputs.led import LED
from tests.TestingSuite import PicoTestBase
import time

class TestLED(PicoTestBase):
    def __init__(self):
        self.led = LED()
    
    def test_on(self):
        self.led.on()
        assert self.led.is_on(), "LED is not on"
        time.sleep(1)

    def test_off(self):
        self.led.off()
        assert not self.led.is_on(), "LED is still on"
        time.sleep(1)