from utils.memory import Memory


class MotionHandler:

    def __init__(self):
        self.memory = Memory()
        self.motion_count = 0
        
    def handle_motion_detection(self, mqtt, rgb_manager):
            # Check PIR and respond to motion (FR2.1, FR2.2, FR2.3)
            from sensors.pir import PIRSensor
            from config import TOPIC_SENSOR_DATA
            from utils.time_sync import TimeSync
            import ujson

            pir = PIRSensor()
            time_sync = TimeSync()

            if pir.is_motion_detected():
                # Request RGB orange for 3 seconds (FR2.2)
                rgb_manager.show('motion', (255, 165, 0), 3)

                # MQTT publish (uses persistent connection)
                payload = ujson.dumps({
                    "sensor_type": "motion",
                    "detected": True,
                    "timestamp": time_sync.get_iso_timestamp()
                })
                if not mqtt.publish(TOPIC_SENSOR_DATA, payload):
                    print("MotionHandler - Error logging motion detection to database")

            del pir, time_sync
            self.memory.collect("After motion handling")