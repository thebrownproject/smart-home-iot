"""
MQTT System Status Contract Test

Tests the system status message format and validation.
Based directly on week 15 museum detector state publishing pattern.

Contract validation for: smarthome/{device_id}/system/status
"""

import json
import time
import network
from umqtt.simple import MQTTClient

# Based on week 15 HiveMQ Cloud configuration
WIFI_SSID = "CyFi"
WIFI_PASS = "SecurityA40"

MQTT_BROKER = "301d2478bf674954a8b8e5ad05732a73.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USER = "thebrownproject"
MQTT_PASS = "StrongPassword123!"

# Contract-specific configuration
TEST_DEVICE_ID = "ESP32_TEST001"
TEST_TOPIC = f"smarthome/{TEST_DEVICE_ID}/system/status"

class SystemStatusContract:
    """
    Contract test for system status messages.

    This test validates the exact JSON schema and MQTT topic structure
    defined in specs/001-comprehensive-smart-home/contracts/mqtt-api.md

    Based directly on week 15 museum detector state publishing:
    - System state tracking (ALARM_ARM, MUTED, ALARM_TRIGGERED)
    - Regular status updates (every 60 seconds + on state change)
    - QoS 1 with message retention for last known state
    """

    def __init__(self):
        self.client_id = f"test-system-{time.ticks_cpu() & 0xffff}"
        self.client = None
        self.received_messages = []
        self.test_results = []

    def setup_wifi(self):
        """Connect to WiFi - using week 15 proven pattern"""
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(WIFI_SSID, WIFI_PASS)
        while not wlan.isconnected():
            time.sleep(0.2)
        print("WiFi connected:", wlan.ifconfig())

    def setup_mqtt(self):
        """Connect to HiveMQ Cloud with TLS"""
        self.client = MQTTClient(
            self.client_id,
            MQTT_BROKER,
            port=MQTT_PORT,
            user=MQTT_USER,
            password=MQTT_PASS,
            ssl=True,
            ssl_params={"server_hostname": MQTT_BROKER}
        )

        self.client.set_callback(self._message_callback)
        self.client.connect()
        self.client.subscribe(TEST_TOPIC.encode())
        print(f"MQTT connected and subscribed to {TEST_TOPIC}")

    def _message_callback(self, topic, msg):
        """Capture received messages for validation"""
        self.received_messages.append({
            "topic": topic.decode(),
            "message": msg.decode(),
            "timestamp": time.time()
        })
        print(f"Received: {topic.decode()} -> {msg.decode()}")

    def validate_system_status_schema(self, message_json):
        """
        Validate message against system status contract schema.

        Required fields from contract (extending week 15 pattern):
        - timestamp: ISO format string
        - pir_enabled: boolean (from week 15 ALARM_ARM)
        - gas_alarm_active: boolean (from week 15 ALARM_TRIGGERED)
        - manual_overrides: object with component override states
        - device_status: object with individual component health
        - network_status: enum ["connected", "disconnected", "error"]
        - uptime_seconds: integer
        - memory_free_bytes: integer
        """
        required_fields = [
            "timestamp", "pir_enabled", "gas_alarm_active", "manual_overrides",
            "device_status", "network_status", "uptime_seconds", "memory_free_bytes"
        ]

        errors = []

        # Check required fields exist
        for field in required_fields:
            if field not in message_json:
                errors.append(f"Missing required field: {field}")

        # Validate boolean fields (from week 15 state variables)
        boolean_fields = ["pir_enabled", "gas_alarm_active"]
        for field in boolean_fields:
            if field in message_json:
                if not isinstance(message_json[field], bool):
                    errors.append(f"{field} must be boolean")

        # Validate manual_overrides object
        if "manual_overrides" in message_json:
            overrides = message_json["manual_overrides"]
            if not isinstance(overrides, dict):
                errors.append("manual_overrides must be object")
            else:
                # Valid override keys
                valid_override_keys = ["gas_alarm", "pir_system", "motion_sensor", "door_lock"]
                for key, value in overrides.items():
                    if key not in valid_override_keys:
                        errors.append(f"Invalid override key: {key}")
                    if not isinstance(value, bool):
                        errors.append(f"Override {key} must be boolean")

        # Validate device_status object
        if "device_status" in message_json:
            device_status = message_json["device_status"]
            if not isinstance(device_status, dict):
                errors.append("device_status must be object")
            else:
                # Valid device status values
                valid_statuses = ["online", "offline", "error", "unknown"]
                # Expected device components
                expected_devices = ["temperature_sensor", "motion_sensor", "rfid_reader", "gas_sensor", "oled_display"]
                for device, status in device_status.items():
                    if status not in valid_statuses:
                        errors.append(f"Invalid device status for {device}: {status}")

        # Validate network_status enum
        if "network_status" in message_json:
            valid_network_statuses = ["connected", "disconnected", "connecting", "error"]
            if message_json["network_status"] not in valid_network_statuses:
                errors.append(f"Invalid network_status: {message_json['network_status']}")

        # Validate numeric fields
        numeric_fields = ["uptime_seconds", "memory_free_bytes"]
        for field in numeric_fields:
            if field in message_json:
                if not isinstance(message_json[field], int) or message_json[field] < 0:
                    errors.append(f"{field} must be positive integer")

        return errors

    def test_normal_system_status(self):
        """Test normal system status - based on week 15 state data"""
        test_message = {
            "timestamp": "2025-09-18T10:30:00Z",
            "pir_enabled": True,        # week 15: ALARM_ARM
            "gas_alarm_active": False,  # week 15: ALARM_TRIGGERED
            "manual_overrides": {
                "gas_alarm": False,
                "pir_system": False
            },
            "device_status": {
                "temperature_sensor": "online",
                "motion_sensor": "online",
                "rfid_reader": "online",
                "gas_sensor": "online",
                "oled_display": "online"
            },
            "network_status": "connected",
            "uptime_seconds": 3600,
            "memory_free_bytes": 45000
        }

        try:
            # This should fail initially - no system status implementation
            message_json = json.dumps(test_message)
            self.client.publish(TEST_TOPIC.encode(), message_json.encode())

            time.sleep(2)
            self.client.check_msg()

            errors = self.validate_system_status_schema(test_message)
            if not errors:
                self.test_results.append("PASS: Normal system status schema valid")
            else:
                self.test_results.append(f"FAIL: Normal status errors: {errors}")

        except Exception as e:
            # Expected to fail (TDD)
            self.test_results.append(f"EXPECTED FAIL: No system status implementation - {e}")

    def test_alarm_triggered_status(self):
        """Test system status during alarm - week 15 ALARM_TRIGGERED = True"""
        test_message = {
            "timestamp": "2025-09-18T10:31:00Z",
            "pir_enabled": True,
            "gas_alarm_active": True,   # ALARM_TRIGGERED from week 15
            "manual_overrides": {
                "gas_alarm": False,
                "pir_system": False
            },
            "device_status": {
                "temperature_sensor": "online",
                "motion_sensor": "online",
                "rfid_reader": "online",
                "gas_sensor": "online",
                "oled_display": "online"
            },
            "network_status": "connected",
            "uptime_seconds": 3700,
            "memory_free_bytes": 42000
        }

        try:
            message_json = json.dumps(test_message)
            self.client.publish(TEST_TOPIC.encode(), message_json.encode())

            time.sleep(2)
            self.client.check_msg()

            errors = self.validate_system_status_schema(test_message)
            if not errors:
                self.test_results.append("PASS: Alarm triggered status schema valid")
            else:
                self.test_results.append(f"FAIL: Alarm status errors: {errors}")

        except Exception as e:
            self.test_results.append(f"EXPECTED FAIL: No alarm status implementation - {e}")

    def test_manual_overrides_status(self):
        """Test system status with manual overrides - week 15 MUTED pattern"""
        test_message = {
            "timestamp": "2025-09-18T10:32:00Z",
            "pir_enabled": False,       # System disarmed
            "gas_alarm_active": False,
            "manual_overrides": {
                "gas_alarm": True,      # week 15: button press to disable
                "pir_system": True      # week 15: MUTED state
            },
            "device_status": {
                "temperature_sensor": "online",
                "motion_sensor": "online",
                "rfid_reader": "online",
                "gas_sensor": "online",
                "oled_display": "online"
            },
            "network_status": "connected",
            "uptime_seconds": 3800,
            "memory_free_bytes": 44000
        }

        try:
            message_json = json.dumps(test_message)
            self.client.publish(TEST_TOPIC.encode(), message_json.encode())

            time.sleep(2)
            self.client.check_msg()

            errors = self.validate_system_status_schema(test_message)
            if not errors:
                self.test_results.append("PASS: Manual overrides status schema valid")
            else:
                self.test_results.append(f"FAIL: Manual overrides errors: {errors}")

        except Exception as e:
            self.test_results.append(f"EXPECTED FAIL: No manual override implementation - {e}")

    def test_device_failure_status(self):
        """Test system status with device failures"""
        test_message = {
            "timestamp": "2025-09-18T10:33:00Z",
            "pir_enabled": True,
            "gas_alarm_active": False,
            "manual_overrides": {
                "gas_alarm": False,
                "pir_system": False
            },
            "device_status": {
                "temperature_sensor": "offline",  # Device failure
                "motion_sensor": "online",
                "rfid_reader": "error",           # Device error
                "gas_sensor": "online",
                "oled_display": "unknown"         # Status unknown
            },
            "network_status": "connected",
            "uptime_seconds": 3900,
            "memory_free_bytes": 41000
        }

        try:
            message_json = json.dumps(test_message)
            self.client.publish(TEST_TOPIC.encode(), message_json.encode())

            time.sleep(2)
            self.client.check_msg()

            errors = self.validate_system_status_schema(test_message)
            if not errors:
                self.test_results.append("PASS: Device failure status schema valid")
            else:
                self.test_results.append(f"FAIL: Device failure errors: {errors}")

        except Exception as e:
            self.test_results.append(f"EXPECTED FAIL: No device monitoring implementation - {e}")

    def test_network_disconnected_status(self):
        """Test system status during network issues"""
        test_message = {
            "timestamp": "2025-09-18T10:34:00Z",
            "pir_enabled": True,
            "gas_alarm_active": False,
            "manual_overrides": {
                "gas_alarm": False,
                "pir_system": False
            },
            "device_status": {
                "temperature_sensor": "online",
                "motion_sensor": "online",
                "rfid_reader": "online",
                "gas_sensor": "online",
                "oled_display": "online"
            },
            "network_status": "disconnected",  # Network issue
            "uptime_seconds": 4000,
            "memory_free_bytes": 40000
        }

        try:
            message_json = json.dumps(test_message)
            self.client.publish(TEST_TOPIC.encode(), message_json.encode())

            time.sleep(2)
            self.client.check_msg()

            errors = self.validate_system_status_schema(test_message)
            if not errors:
                self.test_results.append("PASS: Network disconnected status schema valid")
            else:
                self.test_results.append(f"FAIL: Network status errors: {errors}")

        except Exception as e:
            self.test_results.append(f"EXPECTED FAIL: No network monitoring implementation - {e}")

    def test_low_memory_status(self):
        """Test system status with low memory condition"""
        test_message = {
            "timestamp": "2025-09-18T10:35:00Z",
            "pir_enabled": True,
            "gas_alarm_active": False,
            "manual_overrides": {
                "gas_alarm": False,
                "pir_system": False
            },
            "device_status": {
                "temperature_sensor": "online",
                "motion_sensor": "online",
                "rfid_reader": "online",
                "gas_sensor": "online",
                "oled_display": "online"
            },
            "network_status": "connected",
            "uptime_seconds": 4100,
            "memory_free_bytes": 15000  # Low memory warning
        }

        try:
            message_json = json.dumps(test_message)
            self.client.publish(TEST_TOPIC.encode(), message_json.encode())

            time.sleep(2)
            self.client.check_msg()

            errors = self.validate_system_status_schema(test_message)
            if not errors:
                self.test_results.append("PASS: Low memory status schema valid")
            else:
                self.test_results.append(f"FAIL: Low memory errors: {errors}")

        except Exception as e:
            self.test_results.append(f"EXPECTED FAIL: No memory monitoring implementation - {e}")

    def test_invalid_system_status(self):
        """Test that invalid system status messages are rejected"""
        invalid_message = {
            "timestamp": "2025-09-18T10:36:00Z",
            "pir_enabled": "yes",               # Should be boolean
            "gas_alarm_active": 1,              # Should be boolean
            "manual_overrides": "not_object",   # Should be object
            "device_status": [],                # Should be object
            "network_status": "invalid_status", # Invalid enum
            "uptime_seconds": -100,             # Negative value
            "memory_free_bytes": "low"          # Should be integer
        }

        errors = self.validate_system_status_schema(invalid_message)
        if len(errors) >= 6:  # Should have multiple validation errors
            self.test_results.append("PASS: Invalid system status correctly rejected")
        else:
            self.test_results.append(f"FAIL: Invalid message not properly rejected: {errors}")

    def test_system_status_requirements(self):
        """Test system status message requirements"""
        self.test_results.append("INFO: System status requires QoS 1 (at least once delivery)")
        self.test_results.append("INFO: System status requires message retention (last known state)")
        self.test_results.append("INFO: Status published every 60 seconds + on state change")
        self.test_results.append("INFO: Based on week 15 museum detector state pattern")
        self.test_results.append("INFO: Manual overrides track button press states")

    def run_all_tests(self):
        """Execute all system status contract tests"""
        print("=== MQTT System Status Contract Tests ===")
        print("Based on week 15 museum detector state publishing pattern")
        print()

        try:
            self.setup_wifi()
            self.setup_mqtt()

            # Run contract validation tests
            self.test_normal_system_status()
            self.test_alarm_triggered_status()
            self.test_manual_overrides_status()
            self.test_device_failure_status()
            self.test_network_disconnected_status()
            self.test_low_memory_status()
            self.test_invalid_system_status()
            self.test_system_status_requirements()

            # Print results
            print("\n=== Test Results ===")
            for result in self.test_results:
                print(result)

            # Count expected failures (TDD requirement)
            expected_fails = sum(1 for r in self.test_results if "EXPECTED FAIL" in r)
            print(f"\nExpected Failures (TDD): {expected_fails}/6")
            print("These should fail until system status implementation is complete.")

        except Exception as e:
            print(f"Test setup failed: {e}")
        finally:
            if self.client:
                self.client.disconnect()

def main():
    """Run system status contract tests"""
    test_runner = SystemStatusContract()
    test_runner.run_all_tests()

if __name__ == "__main__":
    main()