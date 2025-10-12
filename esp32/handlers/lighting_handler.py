from utils.memory import Memory

class LightingHandler:
    def __init__(self):
        self.memory = Memory()

    def handle_time_based_lighting(self):
        from utils.time_sync import TimeSync
        from outputs.led import LED
        from display.oled import OLED

        time_sync = TimeSync()
        led = LED()
        oled = OLED()

        if time_sync.is_nighttime():
            led.on()
            oled.show_text("Good Evening", "lights are on")
        else:
            led.off()
            oled.show_text("Good day", "lights are off")

        del time_sync, led, oled
        self.memory.collect("After time-based lighting")