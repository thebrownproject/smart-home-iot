from utils.memory import Memory

class MotionHandler:
    def __init__(self):
        self.memory = Memory()
        
    def handle_motion_detection(self, mqtt, rgb_manager, oled_manager, button_handler):
        from sensors.pir import PIRSensor
        from config import TOPIC_SENSOR_DATA
        from utils.time_sync import TimeSync
        import ujson

        if not button_handler.pir_enabled:
            return

        pir = PIRSensor()
        time_sync = TimeSync()

        if pir.is_motion_detected():
            rgb_manager.show('motion', (255, 165, 0), 3)
            oled_manager.show('motion', "Motion Sensor", 3, "Detected")
            payload = ujson.dumps({
                "sensor_type": "motion",
                "detected": True,
                "timestamp": time_sync.get_iso_timestamp()
            })
            if not mqtt.publish(TOPIC_SENSOR_DATA, payload):
                print("[MotionHandler] MQTT publish failed - motion detection")

        del pir, time_sync
        self.memory.collect("After motion handling")