from utils.memory import Memory

class EnvironmentHandler:
    def __init__(self):
        self.memory = Memory()
        self.last_temp = None
        self.last_humidity = None
        self.loop_counter = 59

    def handle_environment_detection(self, mqtt, oled_manager):
        self.loop_counter += 1
        if self.loop_counter < 60:
            if oled_manager.owner is None and self.last_temp is not None:
                oled_manager.show('environment', f"Temp: {self.last_temp}C", 10, f"Humid: {self.last_humidity}%")
            return
        
        self.loop_counter = 0
        
        import ujson
        from utils.time_sync import TimeSync
        from config import TOPIC_SENSOR_DATA
        from sensors.dht11 import DHT11Sensor

        time_sync = TimeSync()
        dht11 = DHT11Sensor()
        temperature, humidity = dht11.read_data()

        if temperature is None or humidity is None:
            print("EnvironmentHandler - Sensor read failed, skipping update")
            del dht11
            self.memory.collect("After environment handling (error)")
            return
        
        if not (-20 <= temperature <= 60 and 0 <= humidity <= 100):
              print(f"EnvironmentHandler - Invalid reading: {temperature}°C, {humidity}%")
              del dht11, time_sync
              self.memory.collect("After environment handling (invalid)")
              return

        self.last_temp = temperature
        self.last_humidity = humidity
        
        oled_manager.show('environment', f"Temp: {temperature}C", 10, f"Humid: {humidity}%")

        try:
            payload = ujson.dumps({
                "sensor_type": "temperature",
                "value": temperature,
                "unit": "C",
                "timestamp": time_sync.get_iso_timestamp()
            })
            if not mqtt.publish(TOPIC_SENSOR_DATA, payload):
                print("EnvironmentHandler - Temperature publish FAILED")
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
