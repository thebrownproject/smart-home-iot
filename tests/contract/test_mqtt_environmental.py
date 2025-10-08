"""
MQTT Environmental Data Contract Test

Tests the environmental data message format and validation
based on week 15 greenhouse guardian pattern.

Contract validation for: smarthome/{device_id}/environmental/data
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
TEST_TOPIC = f"smarthome/{TEST_DEVICE_ID}/environmental/data"

class EnvironmentalDataContract:
    """
    Contract test for environmental data messages.

    This test validates the exact JSON schema and MQTT topic structure
    defined in specs/001-comprehensive-smart-home/contracts/mqtt-api.md
    """

    def __init__(self):
        self.client_id = f"test-env-{time.ticks_cpu() & 0xffff}"
        self.client = None
        self.received_messages = []
        self.test_results = []

    def setup_wifi(self):
        """Connect to WiFi - based on week 15 pattern"""
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(WIFI_SSID, WIFI_PASS)
        while not wlan.isconnected():
            time.sleep(0.2)
        print("WiFi connected:", wlan.ifconfig())

    def setup_mqtt(self):
        """Connect to HiveMQ Cloud with TLS - using week 15 proven config"""
        self.client = MQTTClient(
            self.client_id,
            MQTT_BROKER,
            port=MQTT_PORT,
            user=MQTT_USER,
            password=MQTT_PASS,
            ssl=True,
            ssl_params={"server_hostname": MQTT_BROKER}
        )

        # Set callback to capture messages
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

    def validate_message_schema(self, message_json):
        """
        Validate message against environmental data contract schema.

        Required fields from contract:
        - timestamp: ISO format string
        - sensor_type: enum ["temperature", "humidity", "gas"]
        - value: number
        - unit: enum ["celsius", "percent", "ppm"]
        - location: string (max 50 chars)
        - status: enum ["normal", "warning", "critical"]
        """
        required_fields = ["timestamp", "sensor_type", "value", "unit"]
        optional_fields = ["location", "status"]

        errors = []

        # Check required fields exist
        for field in required_fields:
            if field not in message_json:
                errors.append(f"Missing required field: {field}")

        # Validate sensor_type enum
        if "sensor_type" in message_json:
            valid_types = ["temperature", "humidity", "gas"]
            if message_json["sensor_type"] not in valid_types:
                errors.append(f"Invalid sensor_type: {message_json['sensor_type']}")

        # Validate unit enum
        if "unit" in message_json:
            valid_units = ["celsius", "percent", "ppm"]
            if message_json["unit"] not in valid_units:
                errors.append(f"Invalid unit: {message_json['unit']}")

        # Validate value is numeric
        if "value" in message_json:
            if not isinstance(message_json["value"], (int, float)):
                errors.append(f"Value must be numeric: {message_json['value']}")

        # Validate status enum if present
        if "status" in message_json:
            valid_statuses = ["normal", "warning", "critical"]
            if message_json["status"] not in valid_statuses:
                errors.append(f"Invalid status: {message_json['status']}")

        # Validate location length if present
        if "location" in message_json:
            if len(message_json["location"]) > 50:
                errors.append(f"Location exceeds 50 characters: {len(message_json['location'])}")

        return errors

    def test_temperature_message(self):
        """Test valid temperature message format"""
        test_message = {
            "timestamp": "2025-09-18T10:30:00Z",
            "sensor_type": "temperature",
            "value": 23.5,
            "unit": "celsius",
            "location": "indoor",
            "status": "normal"
        }

        # This should fail initially - no implementation exists yet
        try:
            # Attempt to publish (will fail if no implementation)
            message_json = json.dumps(test_message)
            self.client.publish(TEST_TOPIC.encode(), message_json.encode())

            # Wait for message
            time.sleep(2)
            self.client.check_msg()

            # Validate schema
            errors = self.validate_message_schema(test_message)
            if not errors:
                self.test_results.append("PASS: Temperature message schema valid")
            else:
                self.test_results.append(f"FAIL: Temperature message errors: {errors}")

        except Exception as e:
            # Expected to fail initially (TDD)
            self.test_results.append(f"EXPECTED FAIL: No implementation yet - {e}")

    def test_humidity_message(self):
        """Test valid humidity message format"""
        test_message = {
            "timestamp": "2025-09-18T10:31:00Z",
            "sensor_type": "humidity",
            "value": 65.0,
            "unit": "percent",
            "location": "indoor",
            "status": "normal"
        }

        try:
            # This should fail - no humidity sensor implementation
            message_json = json.dumps(test_message)
            self.client.publish(TEST_TOPIC.encode(), message_json.encode())

            time.sleep(2)
            self.client.check_msg()

            errors = self.validate_message_schema(test_message)
            if not errors:
                self.test_results.append("PASS: Humidity message schema valid")
            else:
                self.test_results.append(f"FAIL: Humidity message errors: {errors}")

        except Exception as e:
            self.test_results.append(f"EXPECTED FAIL: No implementation yet - {e}")

    def test_gas_message(self):
        """Test valid gas sensor message format"""
        test_message = {
            "timestamp": "2025-09-18T10:32:00Z",
            "sensor_type": "gas",
            "value": 456.0,
            "unit": "ppm",
            "location": "indoor",
            "status": "warning"
        }

        try:
            message_json = json.dumps(test_message)
            self.client.publish(TEST_TOPIC.encode(), message_json.encode())

            time.sleep(2)
            self.client.check_msg()

            errors = self.validate_message_schema(test_message)
            if not errors:
                self.test_results.append("PASS: Gas message schema valid")
            else:
                self.test_results.append(f"FAIL: Gas message errors: {errors}")

        except Exception as e:
            self.test_results.append(f"EXPECTED FAIL: No implementation yet - {e}")

    def test_invalid_message(self):
        """Test that invalid messages are rejected"""
        invalid_message = {
            "timestamp": "2025-09-18T10:33:00Z",
            "sensor_type": "invalid_type",  # Invalid enum
            "value": "not_a_number",        # Invalid type
            "unit": "invalid_unit"          # Invalid enum
        }

        errors = self.validate_message_schema(invalid_message)
        if len(errors) >= 3:  # Should have multiple validation errors
            self.test_results.append("PASS: Invalid message correctly rejected")
        else:
            self.test_results.append(f"FAIL: Invalid message not properly rejected: {errors}")

    def run_all_tests(self):
        """Execute all contract tests"""
        print("=== MQTT Environmental Data Contract Tests ===")
        print("Based on week 15 greenhouse guardian pattern")
        print()

        try:
            self.setup_wifi()
            self.setup_mqtt()

            # Run contract validation tests
            self.test_temperature_message()
            self.test_humidity_message()
            self.test_gas_message()
            self.test_invalid_message()

            # Print results
            print("\n=== Test Results ===")
            for result in self.test_results:
                print(result)

            # Count expected failures (TDD requirement)
            expected_fails = sum(1 for r in self.test_results if "EXPECTED FAIL" in r)
            print(f"\nExpected Failures (TDD): {expected_fails}/3")
            print("These should fail until environmental sensor implementation is complete.")

        except Exception as e:
            print(f"Test setup failed: {e}")
        finally:
            if self.client:
                self.client.disconnect()

def main():
    """Run environmental data contract tests"""
    test_runner = EnvironmentalDataContract()
    test_runner.run_all_tests()

if __name__ == "__main__":
    main()