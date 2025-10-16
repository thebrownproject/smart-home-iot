from utils.memory import Memory

class SteamHandler:
    def __init__(self):
        self.memory = Memory()
        self.flash_count = 0  # Non-blocking flash counter

    def handle_steam_detection(self, mqtt, rgb_manager, oled_manager):
        from sensors.steam import SteamSensor
        from outputs.servo import Servo
        from config import TOPIC_SENSOR_DATA, TOPIC_STATUS_WINDOW
        import ujson
        from utils.time_sync import TimeSync

        steam = SteamSensor()
        window_servo = Servo(pin=5)
        time_sync = TimeSync()

        # Check for new steam detection
        if steam.is_moisture_detected():
            if self.flash_count == 0:  # First detection (not already flashing)
                self.flash_count = 6  # 3 flashes = 6 states (on/off/on/off/on/off)
                window_servo.close()

                # Publish steam detection (FR3.1)
                payload = ujson.dumps({
                    "sensor_type": "steam",
                    "detected": True,
                    "timestamp": time_sync.get_iso_timestamp()
                })
                if not mqtt.publish(TOPIC_SENSOR_DATA, payload):
                    print("SteamHandler - Steam detection MQTT publish FAILED")

                # Publish window status (FR8.4)
                payload = ujson.dumps({
                    "state": "closed",
                    "timestamp": time_sync.get_iso_timestamp()
                })
                if not mqtt.publish(TOPIC_STATUS_WINDOW, payload):
                    print("SteamHandler - Window status MQTT publish FAILED")

        # Non-blocking flash logic (FR3.3 - RGB flashes blue)
        if self.flash_count > 0:
            oled_manager.show('steam', "Steam", 3, "detected")
            self.flash_count -= 1
            if self.flash_count % 2 == 0:
                rgb_manager.show('steam', (0, 0, 255), 1)  # Blue for 1 second
            else:
                rgb_manager.show('steam', (0, 0, 0), 1)  # Off for 1 second

        del steam, window_servo, time_sync
        self.memory.collect("After steam handling")