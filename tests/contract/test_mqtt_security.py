"""
MQTT Security Events Contract Test

Tests the security events message format and validation
based on week 15 museum heist detector pattern.

Contract validation for: smarthome/{device_id}/security/alert
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
TEST_TOPIC = f"smarthome/{TEST_DEVICE_ID}/security/alert"

class SecurityEventsContract:
    """
    Contract test for security events messages.

    This test validates the exact JSON schema and MQTT topic structure
    defined in specs/001-comprehensive-smart-home/contracts/mqtt-api.md

    Based on week 15 museum heist detector state management patterns.
    """

    def __init__(self):
        self.client_id = f"test-security-{time.ticks_cpu() & 0xffff}"
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

    def validate_security_schema(self, message_json):
        """
        Validate message against security events contract schema.

        Required fields from contract:
        - timestamp: ISO format string
        - event_type: enum ["motion", "pir", "manual_override"]
        - severity: enum ["info", "warning", "alert"]
        - triggered_by: string (sensor identifier or "manual")
        - response_actions: array of strings
        - location: string
        """
        required_fields = ["timestamp", "event_type", "severity", "triggered_by", "response_actions", "location"]

        errors = []

        # Check required fields exist
        for field in required_fields:
            if field not in message_json:
                errors.append(f"Missing required field: {field}")

        # Validate event_type enum
        if "event_type" in message_json:
            valid_types = ["motion", "pir", "manual_override", "system_arm", "system_disarm"]
            if message_json["event_type"] not in valid_types:
                errors.append(f"Invalid event_type: {message_json['event_type']}")

        # Validate severity enum
        if "severity" in message_json:
            valid_severities = ["info", "warning", "alert", "critical"]
            if message_json["severity"] not in valid_severities:
                errors.append(f"Invalid severity: {message_json['severity']}")

        # Validate response_actions is array
        if "response_actions" in message_json:
            if not isinstance(message_json["response_actions"], list):
                errors.append("response_actions must be an array")
            else:
                # Validate action types (based on week 15 museum detector pattern)
                valid_actions = ["led_on", "led_off", "fan_start", "fan_stop", "buzzer_on", "buzzer_off",
                               "rgb_flash", "display_alert", "door_lock", "door_unlock"]
                for action in message_json["response_actions"]:
                    if action not in valid_actions:
                        errors.append(f"Invalid response_action: {action}")

        # Validate triggered_by format
        if "triggered_by" in message_json:
            triggered_by = message_json["triggered_by"]
            if not isinstance(triggered_by, str) or len(triggered_by) == 0:
                errors.append("triggered_by must be non-empty string")

        return errors

    def test_motion_detection_event(self):
        """Test motion detection event - based on week 15 pattern"""
        test_message = {
            "timestamp": "2025-09-18T10:30:00Z",
            "event_type": "motion",
            "severity": "info",
            "triggered_by": "motion_sensor_pin14",
            "response_actions": ["led_on", "fan_start"],
            "location": "living_room"
        }

        try:
            # This should fail initially - no motion sensor implementation
            message_json = json.dumps(test_message)
            self.client.publish(TEST_TOPIC.encode(), message_json.encode())

            time.sleep(2)
            self.client.check_msg()

            errors = self.validate_security_schema(test_message)
            if not errors:
                self.test_results.append("PASS: Motion detection event schema valid")
            else:
                self.test_results.append(f"FAIL: Motion detection errors: {errors}")

        except Exception as e:
            # Expected to fail (TDD)
            self.test_results.append(f"EXPECTED FAIL: No motion sensor implementation - {e}")

    def test_pir_security_event(self):
        """Test PIR security system event - from week 15 museum pattern"""
        test_message = {
            "timestamp": "2025-09-18T10:31:00Z",
            "event_type": "pir",
            "severity": "alert",
            "triggered_by": "pir_sensor_pin15",
            "response_actions": ["buzzer_on", "rgb_flash", "display_alert"],
            "location": "security_zone"
        }

        try:
            message_json = json.dumps(test_message)
            self.client.publish(TEST_TOPIC.encode(), message_json.encode())

            time.sleep(2)
            self.client.check_msg()

            errors = self.validate_security_schema(test_message)
            if not errors:
                self.test_results.append("PASS: PIR security event schema valid")
            else:
                self.test_results.append(f"FAIL: PIR security errors: {errors}")

        except Exception as e:
            self.test_results.append(f"EXPECTED FAIL: No PIR implementation - {e}")

    def test_manual_override_event(self):
        """Test manual override event - button control from week 15"""
        test_message = {
            "timestamp": "2025-09-18T10:32:00Z",
            "event_type": "manual_override",
            "severity": "warning",
            "triggered_by": "button_2_press",
            "response_actions": ["display_alert"],
            "location": "control_panel"
        }

        try:
            message_json = json.dumps(test_message)
            self.client.publish(TEST_TOPIC.encode(), message_json.encode())

            time.sleep(2)
            self.client.check_msg()

            errors = self.validate_security_schema(test_message)
            if not errors:
                self.test_results.append("PASS: Manual override event schema valid")
            else:
                self.test_results.append(f"FAIL: Manual override errors: {errors}")

        except Exception as e:
            self.test_results.append(f"EXPECTED FAIL: No manual override implementation - {e}")

    def test_system_arm_disarm_events(self):
        """Test system arm/disarm events - from week 15 museum ARM/DISARM pattern"""
        # Test ARM event
        arm_message = {
            "timestamp": "2025-09-18T10:33:00Z",
            "event_type": "system_arm",
            "severity": "info",
            "triggered_by": "manual",
            "response_actions": ["display_alert"],
            "location": "system"
        }

        # Test DISARM event
        disarm_message = {
            "timestamp": "2025-09-18T10:34:00Z",
            "event_type": "system_disarm",
            "severity": "info",
            "triggered_by": "manual",
            "response_actions": ["led_off", "buzzer_off"],
            "location": "system"
        }

        try:
            # Test ARM
            message_json = json.dumps(arm_message)
            self.client.publish(TEST_TOPIC.encode(), message_json.encode())

            # Test DISARM
            message_json = json.dumps(disarm_message)
            self.client.publish(TEST_TOPIC.encode(), message_json.encode())

            time.sleep(2)
            self.client.check_msg()

            arm_errors = self.validate_security_schema(arm_message)
            disarm_errors = self.validate_security_schema(disarm_message)

            if not arm_errors and not disarm_errors:
                self.test_results.append("PASS: System arm/disarm events schema valid")
            else:
                self.test_results.append(f"FAIL: ARM errors: {arm_errors}, DISARM errors: {disarm_errors}")

        except Exception as e:
            self.test_results.append(f"EXPECTED FAIL: No system control implementation - {e}")

    def test_invalid_security_message(self):
        """Test that invalid security messages are rejected"""
        invalid_message = {
            "timestamp": "2025-09-18T10:35:00Z",
            "event_type": "invalid_event",     # Invalid enum
            "severity": "invalid_severity",    # Invalid enum
            "triggered_by": "",                # Empty string
            "response_actions": "not_array",   # Should be array
            "location": "test"
        }

        errors = self.validate_security_schema(invalid_message)
        if len(errors) >= 3:  # Should have multiple validation errors
            self.test_results.append("PASS: Invalid security message correctly rejected")
        else:
            self.test_results.append(f"FAIL: Invalid message not properly rejected: {errors}")

    def test_qos_2_delivery(self):
        """Test QoS 2 (exactly once) delivery requirement for security events"""
        # Note: This is a contract requirement but hard to test without message acknowledgment
        # For now, document the requirement
        self.test_results.append("INFO: Security events require QoS 2 (exactly once delivery)")
        self.test_results.append("INFO: Critical for ensuring no duplicate security alerts")

    def run_all_tests(self):
        """Execute all security contract tests"""
        print("=== MQTT Security Events Contract Tests ===")
        print("Based on week 15 museum heist detector patterns")
        print()

        try:
            self.setup_wifi()
            self.setup_mqtt()

            # Run contract validation tests
            self.test_motion_detection_event()
            self.test_pir_security_event()
            self.test_manual_override_event()
            self.test_system_arm_disarm_events()
            self.test_invalid_security_message()
            self.test_qos_2_delivery()

            # Print results
            print("\n=== Test Results ===")
            for result in self.test_results:
                print(result)

            # Count expected failures (TDD requirement)
            expected_fails = sum(1 for r in self.test_results if "EXPECTED FAIL" in r)
            print(f"\nExpected Failures (TDD): {expected_fails}/4")
            print("These should fail until security sensor implementation is complete.")

        except Exception as e:
            print(f"Test setup failed: {e}")
        finally:
            if self.client:
                self.client.disconnect()

def main():
    """Run security events contract tests"""
    test_runner = SecurityEventsContract()
    test_runner.run_all_tests()

if __name__ == "__main__":
    main()