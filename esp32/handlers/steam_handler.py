from utils.memory import Memory

class SteamHandler:
    def __init__(self):
        self.memory = Memory()
        self.flash_count = 0

    def handle_steam_detection(self, mqtt, rgb_manager, oled_manager):
        from sensors.steam import SteamSensor
        from outputs.servo import Servo
        from config import TOPIC_SENSOR_DATA, TOPIC_STATUS_WINDOW
        import ujson
        from utils.time_sync import TimeSync

        steam = SteamSensor()
        window_servo = Servo(pin=5)
        time_sync = TimeSync()

        if steam.is_moisture_detected():
            if self.flash_count == 0:
                self.flash_count = 6
                window_servo.close()

                payload = ujson.dumps({
                    "sensor_type": "steam",
                    "detected": True,
                    "timestamp": time_sync.get_iso_timestamp()
                })
                if not mqtt.publish(TOPIC_SENSOR_DATA, payload):
                    print("[SteamHandler] MQTT publish failed - steam detection")

                payload = ujson.dumps({
                    "state": "closed",
                    "timestamp": time_sync.get_iso_timestamp()
                })
                if not mqtt.publish(TOPIC_STATUS_WINDOW, payload):
                    print("[SteamHandler] MQTT publish failed - window status")

        if self.flash_count > 0:
            oled_manager.show('steam', "Steam", 3, "detected")
            self.flash_count -= 1
            if self.flash_count % 2 == 0:
                rgb_manager.show('steam', (0, 0, 255), 1)
            else:
                rgb_manager.show('steam', (0, 0, 0), 1)

        del steam, window_servo, time_sync
        self.memory.collect("After steam handling")