from outputs.servo import Servo
from outputs.servo import DoorServoManager
from tests.TestingSuite import PicoTestBase
import time

class testServo(PicoTestBase):
    def __init__(self):
        self.servo = Servo(13)
    
    def test_open(self):
        self.servo.open()
        assert self.servo.is_open, "Servo is not open"
        time.sleep(1)
    
    def test_close(self):
        self.servo.close()
        assert not self.servo.is_open, "Servo is not closed"
        time.sleep(1)

class testDoorServoManager(PicoTestBase):
    def __init__(self):
        self.door_servo_manager = DoorServoManager()
    
    def test_open(self):
        self.door_servo_manager.open()
        assert self.door_servo_manager.is_open, "Servo is not open"
        time.sleep(1)
    
    def test_close(self):
        self.door_servo_manager.close()
        assert not self.door_servo_manager.is_open, "Servo is not closed"
        time.sleep(1)
    
    def test_update(self):
        self.door_servo_manager.open(duration=3)
        self.door_servo_manager.update()
        assert self.door_servo_manager.countdown == 2, "Countdown is not 2"
        time.sleep(1)
        self.door_servo_manager.update()
        assert self.door_servo_manager.countdown == 1, "Countdown is not 1"
        time.sleep(1)
        self.door_servo_manager.update()
        assert self.door_servo_manager.countdown == 0, "Countdown is not 0"
        assert not self.door_servo_manager.is_open, "Servo is not closed"