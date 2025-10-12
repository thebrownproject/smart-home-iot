from handlers.rfid_handler import RFIDHandler
from comms.mqtt_client import SmartHomeMQTTClient
from comms.wifi_manager import WiFiManager
import time

wifi = WiFiManager()
wifi.connect()

mqtt = SmartHomeMQTTClient()
mqtt.connect()

handler = RFIDHandler()
handler.handle_rfid_detection(mqtt)

print("="*50)
print("Testing RFID Handler")
print("="*50)

for i in range(3):
    print(f"Test {i+1}")
    handler.handle_rfid_detection(mqtt)
    time.sleep(1)

print("="*50)
print("Testing completed")
print("="*50)
