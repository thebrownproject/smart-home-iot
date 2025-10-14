"""
ESP32 Configuration Template

⚠️  IMPORTANT: This is a template file.

To set up your ESP32:
1. Copy this file: `cp config.example.py config.py`
2. Replace placeholder values with your actual credentials
3. Upload config.py to ESP32 (never commit it to git)
"""

# Device Identity
DEVICE_ID = "esp32_main"

# WiFi Configuration
WIFI_SSID = "your_network"
WIFI_PASSWORD = "your_password"

# MQTT
# MQTT Broker (HiveMQ Cloud)
MQTT_BROKER = "your-broker.hivemq.cloud"
MQTT_PORT = 8883  # SSL/TLS
MQTT_USER = "your_username"
MQTT_PASSWORD = "your_password"
# MQTT Topics Outgoing
# Sensor Data
TOPIC_SENSOR_DATA = f"devices/{DEVICE_ID}/data"
# RFID Request
TOPIC_RFID_REQUEST = f"devices/{DEVICE_ID}/rfid/check"
# Status Updates (for web dashboard display - FR8.4, FR8.5)
TOPIC_STATUS_DOOR = f"devices/{DEVICE_ID}/status/door"
TOPIC_STATUS_WINDOW = f"devices/{DEVICE_ID}/status/window"
TOPIC_STATUS_FAN = f"devices/{DEVICE_ID}/status/fan"
# MQTT Topics Incoming
# RFID Response
TOPIC_RFID_RESPONSE = f"devices/{DEVICE_ID}/rfid/response"
# Control Commands (for web remote control - FR9.1, FR9.2, FR9.3)
TOPIC_CONTROL_DOOR = f"devices/{DEVICE_ID}/control/door"
TOPIC_CONTROL_WINDOW = f"devices/{DEVICE_ID}/control/window"
TOPIC_CONTROL_FAN = f"devices/{DEVICE_ID}/control/fan"

# Time Configuration (NTP)
TIMEZONE_OFFSET_HOURS = 10  # AEDT (Melbourne/Sydney) UTC+10
NIGHT_START_HOUR = 20       # 8pm
NIGHT_END_HOUR = 7          # 7am
