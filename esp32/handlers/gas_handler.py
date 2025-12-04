from utils.memory import Memory

class GasHandler:
    def __init__(self):
        self.memory = Memory()
        self.gas_alarm_active = False

    def handle_gas_detection(self, mqtt, rgb_manager, oled_manager, buzzer_manager, button_handler):
        from sensors.gas import GasSensor
        from outputs.fan import Fan
        from config import TOPIC_SENSOR_DATA, TOPIC_STATUS_FAN
        import ujson
        from utils.time_sync import TimeSync

        gas = GasSensor()
        fan = Fan()
        time_sync = TimeSync()

        if not button_handler.gas_alarm_enabled:
            if self.gas_alarm_active:
                self.gas_alarm_active = False
                fan.off()
                buzzer_manager.stop()
            del gas, fan, time_sync
            self.memory.collect("After gas handling (disabled)")
            return

        if not self.gas_alarm_active:
            if gas.is_gas_detected():
                self.gas_alarm_active = True
                fan.on()
                buzzer_manager.start(duration=10)

                payload = ujson.dumps({
                    "sensor_type": "gas",
                    "detected": True,
                    "timestamp": time_sync.get_iso_timestamp()
                })
                if not mqtt.publish(TOPIC_SENSOR_DATA, payload):
                    print("[GasHandler] MQTT publish failed - gas detection")

                payload = ujson.dumps({
                    "state": "on",
                    "timestamp": time_sync.get_iso_timestamp()
                })
                if not mqtt.publish(TOPIC_STATUS_FAN, payload):
                    print("[GasHandler] MQTT publish failed - fan status (on)")

        if self.gas_alarm_active:
            rgb_manager.show('gas', (255, 0, 0), 10)
            oled_manager.show('gas', "Gas", 10, "detected")
            if not gas.is_gas_detected():
                self.gas_alarm_active = False
                fan.off()

                payload = ujson.dumps({
                    "sensor_type": "gas",
                    "detected": False,
                    "timestamp": time_sync.get_iso_timestamp()
                })
                if not mqtt.publish(TOPIC_SENSOR_DATA, payload):
                    print("[GasHandler] MQTT publish failed - gas cleared")

                payload = ujson.dumps({
                    "state": "off",
                    "timestamp": time_sync.get_iso_timestamp()
                })
                if not mqtt.publish(TOPIC_STATUS_FAN, payload):
                    print("[GasHandler] MQTT publish failed - fan status (off)")

        del gas, fan, time_sync
        self.memory.collect("After gas handling")