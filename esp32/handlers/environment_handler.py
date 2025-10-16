from utils.memory import Memory

class EnvironmentHandler:
    def __init__(self):
        self.memory = Memory()
        self.last_temp = None
        self.last_humidity = None
        self.sensor_read_counter = 0  # Loops since last sensor read
        self.mqtt_publish_counter = 0  # Sensor reads since last MQTT publish

    def handle_environment_detection(self, mqtt, oled_manager):
        # PHASE 1: ALWAYS try to reclaim display if idle (instant response)
        if oled_manager.owner is None and self.last_temp is not None:
            oled_manager.show('environment', f"Temp: {self.last_temp}C", 10, f"Humid: {self.last_humidity}%")
            # If display was idle and we reclaimed it, check if we need sensor read
            # If not time yet, exit early to avoid unnecessary work
            if self.sensor_read_counter < 2:
                self.sensor_read_counter += 1
                return

        # PHASE 2: Check if it's time to read sensor (every 2 loops = 2 seconds)
        self.sensor_read_counter += 1
        if self.sensor_read_counter < 2:
            return  # Too soon - DHT11 needs 2+ seconds between reads

        # Reset sensor counter and proceed with read
        self.sensor_read_counter = 0

        # Read sensor
        from sensors.dht11 import DHT11Sensor
        dht11 = DHT11Sensor()
        temperature, humidity = dht11.read_data()

        # Check for sensor read errors
        if temperature is None or humidity is None:
            print("EnvironmentHandler - Sensor read failed, skipping update")
            del dht11
            self.memory.collect("After environment handling (error)")
            return

        # Update display if values changed
        if temperature != self.last_temp or humidity != self.last_humidity:
            oled_manager.show('environment', f"Temp: {temperature}C", 10, f"Humid: {humidity}%")
            self.last_temp = temperature
            self.last_humidity = humidity

        # PHASE 3: Check if it's time to publish to MQTT (every 30 sensor reads = 60 seconds)
        self.mqtt_publish_counter += 1
        if self.mqtt_publish_counter < 30:
            del dht11
            self.memory.collect("After environment handling")
            return  # Not time to publish yet

        # Reset MQTT counter and publish
        self.mqtt_publish_counter = 0

        import ujson
        from utils.time_sync import TimeSync
        from config import TOPIC_SENSOR_DATA

        time_sync = TimeSync()

        # Publish to MQTT (only happens every 60 seconds)
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
