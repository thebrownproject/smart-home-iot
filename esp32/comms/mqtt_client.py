from umqtt.simple import MQTTClient
from config import MQTT_BROKER, MQTT_PORT, MQTT_USER, MQTT_PASSWORD
import time

class SmartHomeMQTTClient:
    def __init__(self):
        self.callbacks = {}
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
    
    def publish(self, topic, payload):
        try:
            self.client.publish(topic, payload)
            return True
        except OSError as e:
            print(f"MQTT publish timeout/error for {topic}: {e}")
            return False
        except Exception as e:
            print(f"Error publishing to MQTT broker ({topic}): {e}")
            return False

    def _dispatch(self, topic, msg):
        """
        Route incoming MQTT messages to the correct handler.

        Flow:
        1. MQTT broker sends message → umqtt library receives it
        2. umqtt calls THIS function (registered via set_callback)
        3. We look up which handler to call based on topic
        4. Call the handler with (topic, msg)

        Example:
        - Message arrives on "devices/esp32_main/rfid/response"
        - _dispatch looks up self.callbacks["devices/esp32_main/rfid/response"]
        - Finds control.handle_rfid_response
        - Calls control.handle_rfid_response(topic, msg)
        """
        topic_str = topic.decode() if isinstance(topic, bytes) else topic
        callback = self.callbacks.get(topic_str)
        if callback:
            callback(topic_str, msg)
        else:
            print(f"No callback found for topic: {topic}")

    def subscribe(self, topic, callback):
        """
        Subscribe to MQTT topic and register handler.

        Note: set_callback is called EVERY time subscribe() is called,
        but umqtt only keeps ONE global callback (_dispatch), which
        then routes to multiple topic-specific handlers via self.callbacks dict.
        """
        try:
            self.callbacks[topic] = callback
            self.client.set_callback(self._dispatch)
            self.client.subscribe(topic)
            print(f"Subscribed to topic: {topic}")
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
