from machine import Pin

BUTTON_GAS_ALARM_PIN = 16
BUTTON_PIR_TOGGLE_PIN = 27

class Button:
    def __init__(self, pin):
        self.button = Pin(pin, Pin.IN, Pin.PULL_UP)

    def is_pressed(self):
        return self.button.value() == 0
