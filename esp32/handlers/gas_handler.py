from utils.memory import Memory

class GasHandler:
    def __init__(self):
        self.memory = Memory()
        self.gas_alarm_active = False

    def handle_gas_detection(self, mqtt):
        # Check gas sensor and respond to gas detection (FR4.1)
        from sensors.gas import GasSensor
        from outputs.rgb import RGB
        from outputs.fan import Fan
        from config import TOPIC_SENSOR_DATA, TOPIC_STATUS_FAN
        import ujson
        from utils.time_sync import TimeSync

        gas = GasSensor()
        rgb = RGB()
        fan = Fan()
        time_sync = TimeSync()

        if not self.gas_alarm_active:
            # Gas detected
            if gas.is_gas_detected():
                self.gas_alarm_active = True
                self.memory.collect("GasHandler - Gas detected")
                rgb.set_color(255, 0, 0)
                fan.on()
                payload = ujson.dumps({
                    "sensor_type": "gas",
                    "detected": True,
                    "timestamp": time_sync.get_iso_timestamp()
                })
                if not mqtt.publish(TOPIC_SENSOR_DATA, payload):
                    print(f"GasHandler - Error logging gas detection to database")
                payload = ujson.dumps({
                    "state": "on",
                    "timestamp": time_sync.get_iso_timestamp()
                })
                if not mqtt.publish(TOPIC_STATUS_FAN, payload):
                    print(f"GasHandler - Error logging fan state to database")

        else:
            # Gas cleared
            if not gas.is_gas_detected():
                self.gas_alarm_active = False
                rgb.off()
                fan.off()
                payload = ujson.dumps({
                    "sensor_type": "gas",
                    "detected": False,
                    "timestamp": time_sync.get_iso_timestamp()
                })
                if not mqtt.publish(TOPIC_SENSOR_DATA, payload):
                    print(f"GasHandler - Error logging gas clearing to database")
                payload = ujson.dumps({
                    "state": "off",
                    "timestamp": time_sync.get_iso_timestamp()
                })
                if not mqtt.publish(TOPIC_STATUS_FAN, payload):
                    print(f"GasHandler - Error logging fan state to database")

        del gas, rgb, fan, time_sync
        self.memory.collect("After gas handling")