from handlers.rfid_handler import RFIDHandler
from comms.mqtt_client import SmartHomeMQTTClient
from comms.wifi_manager import WiFiManager
import time
from utils.memory import Memory

memory = Memory()
memory.collect("Before WiFi connection")

wifi = WiFiManager()
wifi.connect()

memory.collect("After WiFi connection")

mqtt = SmartHomeMQTTClient()
mqtt.connect()

memory.collect("Before RFID handler")

handler = RFIDHandler()

print("="*50)
print("Testing RFID Handler")
print("="*50)

for i in range(5):
    print(f"Test {i+1}")
    handler.handle_rfid_detection(mqtt)
    time.sleep(3)

print("="*50)
print("Testing completed")
print("="*50)
