from utils.memory import Memory

class LightingHandler:
    def __init__(self):
        self.memory = Memory()

    def handle_time_based_lighting(self):
        from utils.time_sync import TimeSync
        from outputs.led import LED

        time_sync = TimeSync()
        led = LED()

        if time_sync.is_nighttime():
            led.on()
        else:
            led.off()

        del time_sync, led
        self.memory.collect("After time-based lighting")