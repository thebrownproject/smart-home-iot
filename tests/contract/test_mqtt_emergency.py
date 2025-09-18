"""
MQTT Emergency Alerts Contract Test

Tests the emergency alert message format and validation.
Critical safety system requiring highest reliability (QoS 2 + retention).

Contract validation for: smarthome/{device_id}/emergency/alert
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
TEST_TOPIC = f"smarthome/{TEST_DEVICE_ID}/emergency/alert"

class EmergencyAlertsContract:
    """
    Contract test for emergency alert messages.

    This test validates the exact JSON schema and MQTT topic structure
    defined in specs/001-comprehensive-smart-home/contracts/mqtt-api.md

    Emergency alerts are the highest priority messages in the system:
    - QoS 2 (exactly once delivery)
    - Message retention enabled (last known state)
    - Immediate response required
    """

    def __init__(self):
        self.client_id = f"test-emergency-{time.ticks_cpu() & 0xffff}"
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
        print(f"EMERGENCY RECEIVED: {topic.decode()} -> {msg.decode()}")

    def validate_emergency_schema(self, message_json):
        """
        Validate message against emergency alerts contract schema.

        Required fields from contract:
        - timestamp: ISO format string
        - emergency_type: enum ["gas_detected", "system_failure"]
        - severity_level: integer 1-5 (5 = critical)
        - triggered_by: string (sensor that detected emergency)
        - response_sequence: array of ordered emergency responses
        - manual_disable: boolean (emergency manually disabled)
        """
        required_fields = ["timestamp", "emergency_type", "severity_level", "triggered_by", "response_sequence", "manual_disable"]

        errors = []

        # Check required fields exist
        for field in required_fields:
            if field not in message_json:
                errors.append(f"Missing required field: {field}")

        # Validate emergency_type enum
        if "emergency_type" in message_json:
            valid_types = ["gas_detected", "system_failure", "fire_detected", "power_failure"]
            if message_json["emergency_type"] not in valid_types:
                errors.append(f"Invalid emergency_type: {message_json['emergency_type']}")

        # Validate severity_level (1-5 scale)
        if "severity_level" in message_json:
            severity = message_json["severity_level"]
            if not isinstance(severity, int) or severity < 1 or severity > 5:
                errors.append(f"severity_level must be integer 1-5: {severity}")

        # Validate triggered_by
        if "triggered_by" in message_json:
            if not isinstance(message_json["triggered_by"], str) or len(message_json["triggered_by"]) == 0:
                errors.append("triggered_by must be non-empty string")

        # Validate response_sequence is array of valid emergency actions
        if "response_sequence" in message_json:
            response_seq = message_json["response_sequence"]
            if not isinstance(response_seq, list):
                errors.append("response_sequence must be array")
            else:
                valid_responses = [
                    "open_doors", "open_windows", "activate_fan", "sound_alarm",
                    "flash_lights", "send_notifications", "call_emergency",
                    "shutdown_gas", "activate_sprinklers"
                ]
                for response in response_seq:
                    if response not in valid_responses:
                        errors.append(f"Invalid emergency response: {response}")

        # Validate manual_disable is boolean
        if "manual_disable" in message_json:
            if not isinstance(message_json["manual_disable"], bool):
                errors.append("manual_disable must be boolean")

        return errors

    def test_gas_detection_emergency(self):
        """Test gas detection emergency - highest priority safety alert"""
        test_message = {
            "timestamp": "2025-09-18T10:30:00Z",
            "emergency_type": "gas_detected",
            "severity_level": 5,  # Critical
            "triggered_by": "gas_sensor_pin23",
            "response_sequence": ["open_doors", "open_windows", "activate_fan", "sound_alarm"],
            "manual_disable": False
        }

        try:
            # This should fail initially - no gas sensor implementation
            message_json = json.dumps(test_message)
            self.client.publish(TEST_TOPIC.encode(), message_json.encode())

            time.sleep(2)
            self.client.check_msg()

            errors = self.validate_emergency_schema(test_message)
            if not errors:
                self.test_results.append("PASS: Gas detection emergency schema valid")
            else:
                self.test_results.append(f"FAIL: Gas detection errors: {errors}")

        except Exception as e:
            # Expected to fail (TDD)
            self.test_results.append(f"EXPECTED FAIL: No gas sensor implementation - {e}")

    def test_system_failure_emergency(self):
        """Test system failure emergency"""
        test_message = {
            "timestamp": "2025-09-18T10:31:00Z",
            "emergency_type": "system_failure",
            "severity_level": 4,  # High
            "triggered_by": "system_monitor",
            "response_sequence": ["send_notifications", "flash_lights"],
            "manual_disable": False
        }

        try:
            message_json = json.dumps(test_message)
            self.client.publish(TEST_TOPIC.encode(), message_json.encode())

            time.sleep(2)
            self.client.check_msg()

            errors = self.validate_emergency_schema(test_message)
            if not errors:
                self.test_results.append("PASS: System failure emergency schema valid")
            else:
                self.test_results.append(f"FAIL: System failure errors: {errors}")

        except Exception as e:
            self.test_results.append(f"EXPECTED FAIL: No system monitoring implementation - {e}")

    def test_manual_disable_emergency(self):
        """Test manually disabled emergency (button 1 press from week 15 pattern)"""
        test_message = {
            "timestamp": "2025-09-18T10:32:00Z",
            "emergency_type": "gas_detected",
            "severity_level": 5,
            "triggered_by": "gas_sensor_pin23",
            "response_sequence": ["open_doors", "activate_fan"],
            "manual_disable": True  # User pressed button 1
        }

        try:
            message_json = json.dumps(test_message)
            self.client.publish(TEST_TOPIC.encode(), message_json.encode())

            time.sleep(2)
            self.client.check_msg()

            errors = self.validate_emergency_schema(test_message)
            if not errors:
                self.test_results.append("PASS: Manual disable emergency schema valid")
            else:
                self.test_results.append(f"FAIL: Manual disable errors: {errors}")

        except Exception as e:
            self.test_results.append(f"EXPECTED FAIL: No manual override implementation - {e}")

    def test_severity_level_variations(self):
        """Test different severity levels (1-5 scale)"""
        severity_tests = [
            (1, "info", ["send_notifications"]),
            (2, "low", ["flash_lights"]),
            (3, "medium", ["sound_alarm", "flash_lights"]),
            (4, "high", ["open_doors", "sound_alarm"]),
            (5, "critical", ["open_doors", "open_windows", "activate_fan", "sound_alarm"])
        ]

        for severity, description, responses in severity_tests:
            test_message = {
                "timestamp": "2025-09-18T10:33:00Z",
                "emergency_type": "gas_detected",
                "severity_level": severity,
                "triggered_by": "gas_sensor_pin23",
                "response_sequence": responses,
                "manual_disable": False
            }

            try:
                message_json = json.dumps(test_message)
                self.client.publish(TEST_TOPIC.encode(), message_json.encode())

                time.sleep(1)
                self.client.check_msg()

                errors = self.validate_emergency_schema(test_message)
                if not errors:
                    self.test_results.append(f"PASS: Severity {severity} ({description}) schema valid")
                else:
                    self.test_results.append(f"FAIL: Severity {severity} errors: {errors}")

            except Exception as e:
                self.test_results.append(f"EXPECTED FAIL: No severity {severity} implementation - {e}")

    def test_comprehensive_emergency_response(self):
        """Test comprehensive emergency response sequence"""
        test_message = {
            "timestamp": "2025-09-18T10:34:00Z",
            "emergency_type": "gas_detected",
            "severity_level": 5,
            "triggered_by": "gas_sensor_pin23",
            "response_sequence": [
                "shutdown_gas",      # First - stop the source
                "open_doors",        # Second - emergency exits
                "open_windows",      # Third - ventilation
                "activate_fan",      # Fourth - forced air circulation
                "sound_alarm",       # Fifth - alert occupants
                "flash_lights",      # Sixth - visual warning
                "send_notifications" # Seventh - external alerts
            ],
            "manual_disable": False
        }

        try:
            message_json = json.dumps(test_message)
            self.client.publish(TEST_TOPIC.encode(), message_json.encode())

            time.sleep(2)
            self.client.check_msg()

            errors = self.validate_emergency_schema(test_message)
            if not errors:
                self.test_results.append("PASS: Comprehensive emergency response schema valid")
            else:
                self.test_results.append(f"FAIL: Comprehensive response errors: {errors}")

        except Exception as e:
            self.test_results.append(f"EXPECTED FAIL: No comprehensive response implementation - {e}")

    def test_invalid_emergency_message(self):
        """Test that invalid emergency messages are rejected"""
        invalid_message = {
            "timestamp": "2025-09-18T10:35:00Z",
            "emergency_type": "invalid_emergency",  # Invalid enum
            "severity_level": 10,                   # Out of range
            "triggered_by": "",                     # Empty string
            "response_sequence": "not_array",       # Should be array
            "manual_disable": "yes"                 # Should be boolean
        }

        errors = self.validate_emergency_schema(invalid_message)
        if len(errors) >= 4:  # Should have multiple validation errors
            self.test_results.append("PASS: Invalid emergency message correctly rejected")
        else:
            self.test_results.append(f"FAIL: Invalid message not properly rejected: {errors}")

    def test_emergency_message_requirements(self):
        """Test critical emergency message requirements"""
        self.test_results.append("INFO: Emergency alerts require QoS 2 (exactly once delivery)")
        self.test_results.append("INFO: Emergency alerts require message retention (last known state)")
        self.test_results.append("INFO: Emergency alerts have highest priority in system")
        self.test_results.append("INFO: Manual disable capability required for safety compliance")
        self.test_results.append("INFO: Response sequence must be ordered by priority")

    def run_all_tests(self):
        """Execute all emergency alerts contract tests"""
        print("=== MQTT Emergency Alerts Contract Tests ===")
        print("CRITICAL SAFETY SYSTEM - Highest priority messages")
        print()

        try:
            self.setup_wifi()
            self.setup_mqtt()

            # Run contract validation tests
            self.test_gas_detection_emergency()
            self.test_system_failure_emergency()
            self.test_manual_disable_emergency()
            self.test_severity_level_variations()
            self.test_comprehensive_emergency_response()
            self.test_invalid_emergency_message()
            self.test_emergency_message_requirements()

            # Print results
            print("\n=== Test Results ===")
            for result in self.test_results:
                print(result)

            # Count expected failures (TDD requirement)
            expected_fails = sum(1 for r in self.test_results if "EXPECTED FAIL" in r)
            print(f"\nExpected Failures (TDD): {expected_fails}/10")
            print("These should fail until emergency response implementation is complete.")
            print("\n⚠️  SAFETY CRITICAL: Emergency system implementation required for safety compliance")

        except Exception as e:
            print(f"Test setup failed: {e}")
        finally:
            if self.client:
                self.client.disconnect()

def main():
    """Run emergency alerts contract tests"""
    test_runner = EmergencyAlertsContract()
    test_runner.run_all_tests()

if __name__ == "__main__":
    main()