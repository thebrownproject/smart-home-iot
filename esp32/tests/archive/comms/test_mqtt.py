from comms.mqtt_client import SmartHomeMQTTClient
import time

mqtt_client = SmartHomeMQTTClient()

print("="*50)
print("MQTT Client Wrapper Test")
print("="*50)

# Callback function - called when messages arrive
def message_callback(topic, msg):
    print("\n✓ Message received!")
    print("  Topic:", topic.decode())
    print("  Message:", msg.decode())

# Connect to MQTT broker
print("\n[1/4] Connecting to MQTT broker...")
if mqtt_client.connect():
    print("✓ Connected")
else:
    print("✗ Connection failed")

# Subscribe to test topic
print("\n[2/4] Subscribing to topic 'home/test'...")
if mqtt_client.subscribe(b"home/test", message_callback):
    print("✓ Subscribed")
else:
    print("✗ Subscribe failed")

# Publish test message
print("\n[3/4] Publishing test message...")
if mqtt_client.publish(b"home/test", b"Hello from ESP32 - Test successful!"):
    print("✓ Published")
else:
    print("✗ Publish failed")

# Check for messages (loop gives MQTT time to deliver)
print("\n[4/4] Checking for messages (5 second timeout)...")
for i in range(5):
    mqtt_client.check_messages()
    time.sleep(1)

# Cleanup
mqtt_client.disconnect()

print("\n" + "="*50)
print("Test Complete!")
print("="*50)
