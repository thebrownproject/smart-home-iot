from utils.memory import Memory

class GasHandler:
    def __init__(self):
        self.memory = Memory()
        self.gas_alarm_active = False

    def handle_gas_detection(self, mqtt, rgb_manager):
        # Check gas sensor and respond to gas detection (FR4.1)
        from sensors.gas import GasSensor
        from outputs.fan import Fan
        from config import TOPIC_SENSOR_DATA, TOPIC_STATUS_FAN
        import ujson
        from utils.time_sync import TimeSync

        gas = GasSensor()
        fan = Fan()
        time_sync = TimeSync()

        if not self.gas_alarm_active:
            # Gas detected - activate alarm
            if gas.is_gas_detected():
                self.gas_alarm_active = True
                fan.on()

                # Publish gas detection (FR4.4)
                payload = ujson.dumps({
                    "sensor_type": "gas",
                    "detected": True,
                    "timestamp": time_sync.get_iso_timestamp()
                })
                if not mqtt.publish(TOPIC_SENSOR_DATA, payload):
                    print(f"GasHandler - Error logging gas detection to database")

                # Publish fan status
                payload = ujson.dumps({
                    "state": "on",
                    "timestamp": time_sync.get_iso_timestamp()
                })
                if not mqtt.publish(TOPIC_STATUS_FAN, payload):
                    print(f"GasHandler - Error logging fan state to database")

        # Keep RGB red while alarm is active (FR4.3)
        if self.gas_alarm_active:
            rgb_manager.show('gas', (255, 0, 0), 11)  # Refresh red for 11 seconds

            # Check if gas has cleared
            if not gas.is_gas_detected():
                self.gas_alarm_active = False
                fan.off()

                # Publish gas cleared
                payload = ujson.dumps({
                    "sensor_type": "gas",
                    "detected": False,
                    "timestamp": time_sync.get_iso_timestamp()
                })
                if not mqtt.publish(TOPIC_SENSOR_DATA, payload):
                    print(f"GasHandler - Error logging gas clearing to database")

                # Publish fan off
                payload = ujson.dumps({
                    "state": "off",
                    "timestamp": time_sync.get_iso_timestamp()
                })
                if not mqtt.publish(TOPIC_STATUS_FAN, payload):
                    print(f"GasHandler - Error logging fan state to database")

        del gas, fan, time_sync
        self.memory.collect("After gas handling")