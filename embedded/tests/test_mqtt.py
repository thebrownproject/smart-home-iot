"""
MQTT Connection Test
====================

Tests MQTT connection to HiveMQ Cloud using credentials from config.py

Usage:
1. Upload config.py to ESP32
2. Upload this file to ESP32
3. Run in REPL: import tests.test_mqtt

Expected output:
- WiFi connected
- MQTT connected to HiveMQ
- Published test message
- Received test message back
"""

import network
import time
import sys
from umqtt.simple import MQTTClient

# Import credentials from config.py
sys.path.append('/')
from config import (
    WIFI_SSID,
    WIFI_PASSWORD,
    MQTT_BROKER,
    MQTT_PORT,
    MQTT_USER,
    MQTT_PASSWORD
)

print("\n" + "="*50)
print("MQTT Connection Test")
print("="*50)

# ============================================================
# WiFi Connection
# ============================================================
print("\n[1/4] Connecting to WiFi...")
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASSWORD)

timeout = 10
while not wlan.isconnected() and timeout > 0:
    time.sleep(1)
    timeout -= 1
    print(f"  Waiting... ({timeout}s left)")

if wlan.isconnected():
    print(f"✓ WiFi connected: {wlan.ifconfig()[0]}")
else:
    print("✗ WiFi connection failed!")
    sys.exit(1)

# ============================================================
# MQTT Setup
# ============================================================
print("\n[2/4] Setting up MQTT client...")

CLIENT_ID = "test-esp32-" + str(time.ticks_cpu() & 0xffff)
TOPIC_TEST = b"smarthome/test"

print(f"  Client ID: {CLIENT_ID}")
print(f"  Broker: {MQTT_BROKER}:{MQTT_PORT}")

client = MQTTClient(
    CLIENT_ID,
    MQTT_BROKER,
    port=MQTT_PORT,
    user=MQTT_USER,
    password=MQTT_PASSWORD,
    ssl=True,
    ssl_params={"server_hostname": MQTT_BROKER}
)

# Message callback
def mqtt_callback(topic, msg):
    print(f"\n[4/4] ✓ Received message!")
    print(f"  Topic: {topic.decode()}")
    print(f"  Message: {msg.decode()}")

client.set_callback(mqtt_callback)

# ============================================================
# MQTT Connection
# ============================================================
print("\n[3/4] Connecting to MQTT broker...")
try:
    client.connect()
    print("✓ Connected to HiveMQ Cloud")

    # Subscribe to test topic
    client.subscribe(TOPIC_TEST)
    print(f"✓ Subscribed to: {TOPIC_TEST.decode()}")

    # Publish test message
    test_message = b"Hello from ESP32 - MQTT test successful!"
    client.publish(TOPIC_TEST, test_message)
    print(f"✓ Published: {test_message.decode()}")

    # Wait for message (should receive our own published message)
    print("\n  Waiting for message (5s timeout)...")
    for i in range(5):
        client.check_msg()
        time.sleep(1)

    # Cleanup
    client.disconnect()
    print("\n" + "="*50)
    print("Test Complete - MQTT connection working! ✓")
    print("="*50 + "\n")

except Exception as e:
    print(f"\n✗ MQTT Error: {e}")
    print("\nTroubleshooting:")
    print("  - Check MQTT_BROKER URL in config.py")
    print("  - Verify MQTT_USER and MQTT_PASSWORD")
    print("  - Ensure HiveMQ cluster is active (free tier hibernates)")
    print("  - Check port is 8883 (SSL/TLS)")
