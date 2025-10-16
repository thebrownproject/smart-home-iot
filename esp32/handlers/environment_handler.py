from utils.memory import Memory

class EnvironmentHandler:
    def __init__(self):
        self.memory = Memory()
        self.last_temp = None
        self.last_humidity = None

    def handle_environment_detection(self, mqtt, oled_manager):
        from sensors.dht11 import DHT11Sensor
        import ujson
        from utils.time_sync import TimeSync
        from config import TOPIC_SENSOR_DATA

        dht11 = DHT11Sensor()
        time_sync = TimeSync()
        temperature, humidity = dht11.read_data()

        # Check for sensor read errors
        if temperature is None or humidity is None:
            print("EnvironmentHandler - Sensor read failed, skipping update")
            del dht11, time_sync
            self.memory.collect("After environment handling (error)")
            return

        # Only update display if values changed (prevents unnecessary redraws)
        if temperature != self.last_temp or humidity != self.last_humidity:
            oled_manager.show('environment', f"Temp: {temperature}C", 10, f"Humid: {humidity}%")
            self.last_temp = temperature
            self.last_humidity = humidity

        # Publish to MQTT with error handling (connection may be unstable)
        try:
            # Publish temperature
            payload = ujson.dumps({
                "sensor_type": "temperature",
                "value": temperature,
                "unit": "C",
                "timestamp": time_sync.get_iso_timestamp()
            })
            if not mqtt.publish(TOPIC_SENSOR_DATA, payload):
                print("EnvironmentHandler - Temperature publish FAILED")
            # Publish humidity
            payload = ujson.dumps({
                "sensor_type": "humidity",
                "value": humidity,
                "unit": "%",
                "timestamp": time_sync.get_iso_timestamp()
            })
            if not mqtt.publish(TOPIC_SENSOR_DATA, payload):
                print("EnvironmentHandler - Humidity publish FAILED")
        except Exception as e:
            print(f"EnvironmentHandler - Unexpected error: {e}")

        del dht11, time_sync
        self.memory.collect("After environment handling")