from utils.memory import Memory

class EnvironmentHandler:
    def __init__(self):
        self.memory = Memory()

    def handle_environment_detection(self, mqtt):
        from sensors.dht11 import DHT11Sensor
        from display.oled import OLED
        import json

        dht11 = DHT11Sensor()
        oled = OLED()

        temperature, humidity = dht11.read_data()

        # Check for sensor read errors
        if temperature is None or humidity is None:
            print("EnvironmentHandler - Sensor read failed, skipping update")
            del dht11, oled
            self.memory.collect("After environment handling (error)")
            return

        oled.show_temp_humidity(temperature, humidity)

        # Format MQTT payloads as JSON for web dashboard
        temp_payload = json.dumps({"value": temperature, "unit": "C"})
        humidity_payload = json.dumps({"value": humidity, "unit": "%"})

        # Publish to MQTT with error handling (connection may be unstable)
        try:
            print(f"EnvironmentHandler - Publishing temp: {temp_payload}")
            if mqtt.publish("home/temperature", temp_payload):
                print("EnvironmentHandler - Temperature MQTT Publish OK")
            else:
                print("EnvironmentHandler - Temperature MQTT Publish FAILED")
        except Exception as e:
            print(f"EnvironmentHandler - Temperature MQTT Error: {e}")

        try:
            print(f"EnvironmentHandler - Publishing humidity: {humidity_payload}")
            if mqtt.publish("home/humidity", humidity_payload):
                print("EnvironmentHandler - Humidity MQTT Publish OK")
            else:
                print("EnvironmentHandler - Humidity MQTT Publish FAILED")
        except Exception as e:
            print(f"EnvironmentHandler - Humidity MQTT Error: {e}")

        del dht11, oled
        self.memory.collect("After environment handling")