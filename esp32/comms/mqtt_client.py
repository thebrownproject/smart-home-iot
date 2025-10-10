from umqtt.simple import MQTTClient
from config import MQTT_BROKER, MQTT_PORT, MQTT_USER, MQTT_PASSWORD
import time


class SmartHomeMQTTClient:
    def __init__(self):
        self.client_id = "test-esp32-" + str(time.ticks_cpu() & 0xffff)
        self.client = MQTTClient(
            self.client_id,
            MQTT_BROKER,
            port=MQTT_PORT,
            user=MQTT_USER,
            password=MQTT_PASSWORD,
            ssl=True,
            ssl_params={"server_hostname": MQTT_BROKER}
        )
    
    def connect(self):
        try:
            self.client.connect()
            print("Connected to MQTT broker")
            return True
        except Exception as e:
            print("Error connecting to MQTT broker:", e)
            return False
    
    def disconnect(self):
        try:
            self.client.disconnect()
            return True
        except Exception as e:
            print("Error disconnecting from MQTT broker:", e)
            return False
    
    def publish(self, topic, payload):
        try:
            self.client.publish(topic, payload)
            return True
        except Exception as e:
            print("Error publishing to MQTT broker:", e)
            return False
    
    def subscribe(self, topic, callback):
        try:
            self.client.set_callback(callback)
            self.client.subscribe(topic)
            return True
        except Exception as e:
            print("Error subscribing to MQTT broker:", e)
            return False

    def check_messages(self):
        try:
            self.client.check_msg()
            return True
        except Exception as e:
            print("Error checking messages from MQTT broker:", e)
            return False
