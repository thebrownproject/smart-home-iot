"""
ESP32 Configuration Template

⚠️  IMPORTANT: This is a template file.

To set up your ESP32:
1. Copy this file: `cp config.example.py config.py`
2. Replace placeholder values with your actual credentials
3. Upload config.py to ESP32 (never commit it to git)
"""

# WiFi Configuration
WIFI_SSID = "CyFi"
WIFI_PASSWORD = "SecurityA40"

# MQTT Broker (HiveMQ Cloud)
MQTT_BROKER = "301d2478bf674954a8b8e5ad05732a73.s1.eu.hivemq.cloud"
MQTT_PORT = 8883  # SSL/TLS
MQTT_USER = "thebrownproject"
MQTT_PASSWORD = "StrongPassword123!"

# Supabase (Direct HTTP)
SUPABASE_URL = "https://uehfuypnccdqvdssknqq.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVlaGZ1eXBuY2NkcXZkc3NrbnFxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk4ODMwNzksImV4cCI6MjA3NTQ1OTA3OX0.r4L-PRdbqae7nm23-H3FQQFNWnnh4kkA_HrlwGjnPE8"
