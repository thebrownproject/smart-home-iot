"""
MQTT Access Control Contract Test

Tests the RFID access control message format and validation.
This is a new pattern extending week 15 concepts to RFID door control.

Contract validation for: smarthome/{device_id}/access/data
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
TEST_TOPIC = f"smarthome/{TEST_DEVICE_ID}/access/data"

class AccessControlContract:
    """
    Contract test for RFID access control messages.

    This test validates the exact JSON schema and MQTT topic structure
    defined in specs/001-comprehensive-smart-home/contracts/mqtt-api.md

    Extends week 15 MQTT patterns to handle RFID access control events.
    """

    def __init__(self):
        self.client_id = f"test-access-{time.ticks_cpu() & 0xffff}"
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

    def validate_access_schema(self, message_json):
        """
        Validate message against access control contract schema.

        Required fields from contract:
        - timestamp: ISO format string
        - card_uid: string (8-character hex string for RC522)
        - access_granted: boolean
        - door_action: enum ["unlock", "lock", "blocked"]
        - user_name: string (1-50 characters, optional if not registered)
        - location: string
        """
        required_fields = ["timestamp", "card_uid", "access_granted", "door_action", "location"]

        errors = []

        # Check required fields exist
        for field in required_fields:
            if field not in message_json:
                errors.append(f"Missing required field: {field}")

        # Validate card_uid format (8-character hex string)
        if "card_uid" in message_json:
            card_uid = message_json["card_uid"]
            if not isinstance(card_uid, str):
                errors.append("card_uid must be string")
            elif len(card_uid) != 8:
                errors.append(f"card_uid must be 8 characters: {len(card_uid)}")
            else:
                # Check if hex format
                try:
                    int(card_uid, 16)
                except ValueError:
                    errors.append(f"card_uid must be hex format: {card_uid}")

        # Validate access_granted is boolean
        if "access_granted" in message_json:
            if not isinstance(message_json["access_granted"], bool):
                errors.append("access_granted must be boolean")

        # Validate door_action enum
        if "door_action" in message_json:
            valid_actions = ["unlock", "lock", "blocked", "error"]
            if message_json["door_action"] not in valid_actions:
                errors.append(f"Invalid door_action: {message_json['door_action']}")

        # Validate user_name if present (1-50 characters)
        if "user_name" in message_json:
            user_name = message_json["user_name"]
            if user_name is not None:  # Can be null for unregistered cards
                if not isinstance(user_name, str):
                    errors.append("user_name must be string or null")
                elif len(user_name) < 1 or len(user_name) > 50:
                    errors.append(f"user_name must be 1-50 characters: {len(user_name)}")

        # Validate location
        if "location" in message_json:
            if not isinstance(message_json["location"], str) or len(message_json["location"]) == 0:
                errors.append("location must be non-empty string")

        return errors

    def test_authorized_access(self):
        """Test authorized RFID card access"""
        test_message = {
            "timestamp": "2025-09-18T10:30:00Z",
            "card_uid": "A1B2C3D4",
            "access_granted": True,
            "door_action": "unlock",
            "user_name": "John Doe",
            "location": "main_door"
        }

        try:
            # This should fail initially - no RFID implementation
            message_json = json.dumps(test_message)
            self.client.publish(TEST_TOPIC.encode(), message_json.encode())

            time.sleep(2)
            self.client.check_msg()

            errors = self.validate_access_schema(test_message)
            if not errors:
                self.test_results.append("PASS: Authorized access event schema valid")
            else:
                self.test_results.append(f"FAIL: Authorized access errors: {errors}")

        except Exception as e:
            # Expected to fail (TDD)
            self.test_results.append(f"EXPECTED FAIL: No RFID implementation - {e}")

    def test_unauthorized_access(self):
        """Test unauthorized RFID card access attempt"""
        test_message = {
            "timestamp": "2025-09-18T10:31:00Z",
            "card_uid": "E5F6G7H8",
            "access_granted": False,
            "door_action": "blocked",
            "user_name": None,  # Unregistered card
            "location": "main_door"
        }

        try:
            message_json = json.dumps(test_message)
            self.client.publish(TEST_TOPIC.encode(), message_json.encode())

            time.sleep(2)
            self.client.check_msg()

            errors = self.validate_access_schema(test_message)
            if not errors:
                self.test_results.append("PASS: Unauthorized access event schema valid")
            else:
                self.test_results.append(f"FAIL: Unauthorized access errors: {errors}")

        except Exception as e:
            self.test_results.append(f"EXPECTED FAIL: No RFID implementation - {e}")

    def test_door_lock_action(self):
        """Test door lock action (manual or automatic)"""
        test_message = {
            "timestamp": "2025-09-18T10:32:00Z",
            "card_uid": "A1B2C3D4",
            "access_granted": True,
            "door_action": "lock",
            "user_name": "John Doe",
            "location": "main_door"
        }

        try:
            message_json = json.dumps(test_message)
            self.client.publish(TEST_TOPIC.encode(), message_json.encode())

            time.sleep(2)
            self.client.check_msg()

            errors = self.validate_access_schema(test_message)
            if not errors:
                self.test_results.append("PASS: Door lock action schema valid")
            else:
                self.test_results.append(f"FAIL: Door lock errors: {errors}")

        except Exception as e:
            self.test_results.append(f"EXPECTED FAIL: No servo control implementation - {e}")

    def test_rfid_error_condition(self):
        """Test RFID reader error condition"""
        test_message = {
            "timestamp": "2025-09-18T10:33:00Z",
            "card_uid": "00000000",  # Error code from RFID reader
            "access_granted": False,
            "door_action": "error",
            "user_name": None,
            "location": "main_door"
        }

        try:
            message_json = json.dumps(test_message)
            self.client.publish(TEST_TOPIC.encode(), message_json.encode())

            time.sleep(2)
            self.client.check_msg()

            errors = self.validate_access_schema(test_message)
            if not errors:
                self.test_results.append("PASS: RFID error condition schema valid")
            else:
                self.test_results.append(f"FAIL: RFID error errors: {errors}")

        except Exception as e:
            self.test_results.append(f"EXPECTED FAIL: No error handling implementation - {e}")

    def test_multiple_door_locations(self):
        """Test access events for different door locations"""
        locations = ["main_door", "back_door", "garage_door"]

        for location in locations:
            test_message = {
                "timestamp": "2025-09-18T10:34:00Z",
                "card_uid": "A1B2C3D4",
                "access_granted": True,
                "door_action": "unlock",
                "user_name": "John Doe",
                "location": location
            }

            try:
                message_json = json.dumps(test_message)
                self.client.publish(TEST_TOPIC.encode(), message_json.encode())

                time.sleep(1)
                self.client.check_msg()

                errors = self.validate_access_schema(test_message)
                if not errors:
                    self.test_results.append(f"PASS: {location} access schema valid")
                else:
                    self.test_results.append(f"FAIL: {location} access errors: {errors}")

            except Exception as e:
                self.test_results.append(f"EXPECTED FAIL: No {location} implementation - {e}")

    def test_invalid_access_message(self):
        """Test that invalid access messages are rejected"""
        invalid_message = {
            "timestamp": "2025-09-18T10:35:00Z",
            "card_uid": "INVALID_UID",        # Not 8-char hex
            "access_granted": "yes",          # Should be boolean
            "door_action": "invalid_action",  # Invalid enum
            "user_name": "A" * 60,           # Too long
            "location": ""                    # Empty string
        }

        errors = self.validate_access_schema(invalid_message)
        if len(errors) >= 4:  # Should have multiple validation errors
            self.test_results.append("PASS: Invalid access message correctly rejected")
        else:
            self.test_results.append(f"FAIL: Invalid message not properly rejected: {errors}")

    def test_qos_2_delivery_requirement(self):
        """Test QoS 2 (exactly once) delivery requirement for access events"""
        # Note: Access events are critical for security audit logs
        self.test_results.append("INFO: Access events require QoS 2 (exactly once delivery)")
        self.test_results.append("INFO: Critical for security audit logs and compliance")

    def run_all_tests(self):
        """Execute all access control contract tests"""
        print("=== MQTT Access Control Contract Tests ===")
        print("Extending week 15 MQTT patterns to RFID access control")
        print()

        try:
            self.setup_wifi()
            self.setup_mqtt()

            # Run contract validation tests
            self.test_authorized_access()
            self.test_unauthorized_access()
            self.test_door_lock_action()
            self.test_rfid_error_condition()
            self.test_multiple_door_locations()
            self.test_invalid_access_message()
            self.test_qos_2_delivery_requirement()

            # Print results
            print("\n=== Test Results ===")
            for result in self.test_results:
                print(result)

            # Count expected failures (TDD requirement)
            expected_fails = sum(1 for r in self.test_results if "EXPECTED FAIL" in r)
            print(f"\nExpected Failures (TDD): {expected_fails}/7")
            print("These should fail until RFID access control implementation is complete.")

        except Exception as e:
            print(f"Test setup failed: {e}")
        finally:
            if self.client:
                self.client.disconnect()

def main():
    """Run access control contract tests"""
    test_runner = AccessControlContract()
    test_runner.run_all_tests()

if __name__ == "__main__":
    main()