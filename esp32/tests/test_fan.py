from outputs.fan import Fan
from tests.TestingSuite import PicoTestBase
import time

class TestFan(PicoTestBase):
    def __init__(self):
        self.fan = Fan()

    def test_on(self):
        self.fan.on()
        assert self.fan.is_on(), "Fan is not running"
        time.sleep(1)

    def test_off(self):
        self.fan.off()
        assert not self.fan.is_on(), "Fan is still running"
        time.sleep(1)


