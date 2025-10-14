from utils.memory import Memory


class MotionHandler:

    def __init__(self):
        self.memory = Memory()
        self.motion_count = 0
        
    def handle_motion_detection(self, mqtt):
            """Check PIR and respond to motion (FR2.1, FR2.2, FR2.3)"""
            from sensors.pir import PIRSensor
            from outputs.rgb import RGB
            from config import TOPIC_SENSOR_DATA
            from utils.time_sync import TimeSync
            import ujson

            pir = PIRSensor()
            rgb = RGB()
            time_sync = TimeSync()

            if pir.is_motion_detected():
                self.motion_count = 3

                # Set RGB to orange (FR2.2)
                rgb.set_color(255, 165, 0)  # Orange

                # MQTT publish (uses persistent connection)
                payload = ujson.dumps({
                    "sensor_type": "motion",
                    "detected": True,
                    "timestamp": time_sync.get_iso_timestamp()
                })
                if not mqtt.publish(TOPIC_SENSOR_DATA, payload):
                    print("MotionHandler - Error logging motion detection to database")

            # Don't turn off RGB - let state machine handle priority (T1.29)
            if self.motion_count > 0:  # Only count down if timer active
                self.motion_count -= 1
                if self.motion_count == 0:  # Turn off when timer expires
                    rgb.off()
            del pir, rgb, time_sync
            self.memory.collect("After motion handling")