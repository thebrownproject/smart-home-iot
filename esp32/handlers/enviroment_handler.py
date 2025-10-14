from utils.memory import Memory

class EnvironmentHandler:
    def __init__(self):
        self.memory = Memory()

    def handle_environment_detection(self, mqtt):
        from sensors.dht11 import DHT11Sensor
        from display.oled import OLED
        import ujson
        from utils.time_sync import TimeSync
        from config import TOPIC_SENSOR_DATA

        dht11 = DHT11Sensor()
        oled = OLED()
        time_sync = TimeSync()
        temperature, humidity = dht11.read_data()

        # Check for sensor read errors
        if temperature is None or humidity is None:
            print("EnvironmentHandler - Sensor read failed, skipping update")
            del dht11, oled, time_sync
            self.memory.collect("After environment handling (error)")
            return

        # Display temperature and humidity on OLED
        oled.show_temp_humidity(temperature, humidity)

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

        del dht11, oled, time_sync
        self.memory.collect("After environment handling")