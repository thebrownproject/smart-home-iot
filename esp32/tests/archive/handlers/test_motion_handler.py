from handlers.motion_handler import MotionHandler
import time
from comms.mqtt_client import SmartHomeMQTTClient
from comms.wifi_manager import WiFiManager

# Connect to WiFi first (required for MQTT)
wifi = WiFiManager()
wifi.connect()

mqtt = SmartHomeMQTTClient()
mqtt.connect()

motion_handler = MotionHandler()

print("="*50)
print("Testing Motion Handler")
print("="*50)

for i in range(3):
    print(f"Test {i+1}")
    motion_handler.handle_motion_detection(mqtt)
    time.sleep(1)

print("="*50)
print("Testing completed")
print("="*50)