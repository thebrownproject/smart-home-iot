"""
DHT11 Sensor Unit Tests

LEARNING OBJECTIVES:
1. Understand unit testing for embedded systems
2. Learn how to mock hardware components
3. Master test-driven development (TDD) concepts
4. Practice edge case testing for sensor validation

TESTING CONCEPTS:
- Unit tests verify individual components work correctly
- Mocking simulates hardware without needing physical devices
- Edge case testing ensures robustness in unusual conditions
- TDD helps design better interfaces by thinking about usage first
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import time

# Import the classes we're testing
from src.sensors.dht11 import DHT11Sensor, DHT11Reading
from src.sensors.base_sensor import SensorStatus, SensorError

class TestDHT11Reading(unittest.TestCase):
    """
    Test the DHT11Reading data structure.

    LEARNING NOTE: We test data structures separately from hardware
    because they contain business logic (like temperature conversion)
    that we can test without hardware dependencies.
    """

    def setUp(self):
        """Set up test data before each test method."""
        self.reading = DHT11Reading(temperature_c=25.0, humidity_percent=60.0)

    def test_temperature_conversion(self):
        """Test Celsius to Fahrenheit conversion."""
        # 25°C should equal 77°F
        expected_f = 77.0
        self.assertAlmostEqual(self.reading.temperature_f, expected_f, places=1)

        # Test freezing point: 0°C = 32°F
        freezing_reading = DHT11Reading(0.0, 50.0)
        self.assertAlmostEqual(freezing_reading.temperature_f, 32.0, places=1)

    def test_string_representation(self):
        """Test the string format of readings."""
        expected = "DHT11: 25.0°C, 60.0% RH"
        self.assertEqual(str(self.reading), expected)

    def test_heat_index_placeholder(self):
        """
        Test heat index calculation (currently returns temperature).

        LEARNING EXERCISE: Once you implement the heat_index property,
        update this test to verify correct heat index calculations.
        """
        # Currently returns temperature as placeholder
        self.assertEqual(self.reading.heat_index, self.reading.temperature_c)

        # TODO: Add real heat index test cases once implemented
        # Example test cases to implement:
        # - 27°C, 70% humidity should have higher heat index than temperature
        # - Low humidity should have heat index close to temperature
        # - Very high humidity + temperature should have much higher heat index

class TestDHT11Sensor(unittest.TestCase):
    """
    Test the DHT11Sensor class.

    LEARNING NOTE: Testing sensor classes requires mocking the hardware
    because we can't rely on physical sensors being connected during
    automated testing. This teaches separation of concerns between
    hardware interface and business logic.
    """

    def setUp(self):
        """Set up test sensor before each test method."""
        # Mock the hardware Pin to avoid hardware dependencies
        with patch('src.sensors.dht11.Pin'):
            self.sensor = DHT11Sensor("Test DHT11", pin_number=17)

    @patch('src.sensors.dht11.dht.DHT11')
    @patch('src.sensors.dht11.Pin')
    def test_initialization_success(self, mock_pin, mock_dht11):
        """Test successful sensor initialization."""
        # Mock successful hardware initialization
        mock_dht_device = MagicMock()
        mock_dht11.return_value = mock_dht_device

        # Test initialization
        sensor = DHT11Sensor("Test DHT11", pin_number=17)
        success = sensor.initialize()

        self.assertTrue(success)
        self.assertEqual(sensor.status, SensorStatus.READY)
        mock_dht11.assert_called_once()

    @patch('src.sensors.dht11.dht.DHT11')
    @patch('src.sensors.dht11.Pin')
    def test_initialization_failure(self, mock_pin, mock_dht11):
        """Test sensor initialization failure handling."""
        # Mock hardware initialization failure
        mock_dht11.side_effect = Exception("Hardware not found")

        sensor = DHT11Sensor("Test DHT11", pin_number=17)
        success = sensor.initialize()

        self.assertFalse(success)
        self.assertEqual(sensor.status, SensorStatus.FAILED)

    @patch('src.sensors.dht11.dht.DHT11')
    @patch('src.sensors.dht11.Pin')
    def test_successful_reading(self, mock_pin, mock_dht11):
        """Test successful sensor reading."""
        # Set up mock DHT device
        mock_dht_device = MagicMock()
        mock_dht_device.temperature.return_value = 22.5
        mock_dht_device.humidity.return_value = 55.0
        mock_dht11.return_value = mock_dht_device

        # Initialize sensor
        sensor = DHT11Sensor("Test DHT11", pin_number=17)
        sensor.initialize()

        # Test reading
        reading = sensor.read()

        self.assertIsInstance(reading, DHT11Reading)
        self.assertEqual(reading.temperature_c, 22.5)
        self.assertEqual(reading.humidity_percent, 55.0)
        mock_dht_device.measure.assert_called()

    @patch('src.sensors.dht11.dht.DHT11')
    @patch('src.sensors.dht11.Pin')
    def test_reading_validation_failure(self, mock_pin, mock_dht11):
        """Test handling of invalid sensor readings."""
        # Set up mock DHT device with invalid readings
        mock_dht_device = MagicMock()
        mock_dht_device.temperature.return_value = -10.0  # Below DHT11 range
        mock_dht_device.humidity.return_value = 150.0     # Above 100%
        mock_dht11.return_value = mock_dht_device

        # Initialize sensor
        sensor = DHT11Sensor("Test DHT11", pin_number=17)
        sensor.initialize()

        # Test reading - should return None due to validation failure
        reading = sensor.read()

        self.assertIsNone(reading)
        self.assertEqual(sensor.status, SensorStatus.ERROR)

    @patch('src.sensors.dht11.dht.DHT11')
    @patch('src.sensors.dht11.Pin')
    def test_communication_error_handling(self, mock_pin, mock_dht11):
        """Test handling of sensor communication errors."""
        # Set up mock DHT device that raises communication error
        mock_dht_device = MagicMock()
        mock_dht_device.measure.side_effect = OSError("Communication timeout")
        mock_dht11.return_value = mock_dht_device

        # Initialize sensor
        sensor = DHT11Sensor("Test DHT11", pin_number=17)
        sensor.initialize()

        # Test reading - should handle error gracefully
        reading = sensor.read()

        self.assertIsNone(reading)
        self.assertEqual(sensor.error_count, 1)

    def test_sample_rate_limiting(self):
        """Test that sample rate is limited to DHT11 maximum."""
        # DHT11 should limit sample rate to 0.5 Hz
        sensor = DHT11Sensor("Test DHT11", pin_number=17, sample_rate=2.0)
        self.assertEqual(sensor.sample_rate, 0.5)

    @patch('src.sensors.dht11.dht.DHT11')
    @patch('src.sensors.dht11.Pin')
    def test_convenience_methods(self, mock_pin, mock_dht11):
        """Test convenience methods for getting specific values."""
        # Set up mock DHT device
        mock_dht_device = MagicMock()
        mock_dht_device.temperature.return_value = 20.0
        mock_dht_device.humidity.return_value = 65.0
        mock_dht11.return_value = mock_dht_device

        # Initialize sensor
        sensor = DHT11Sensor("Test DHT11", pin_number=17)
        sensor.initialize()

        # Test convenience methods
        temp_c = sensor.get_temperature_celsius()
        temp_f = sensor.get_temperature_fahrenheit()
        humidity = sensor.get_humidity()

        self.assertEqual(temp_c, 20.0)
        self.assertAlmostEqual(temp_f, 68.0, places=1)  # 20°C = 68°F
        self.assertEqual(humidity, 65.0)

class TestEdgeCases(unittest.TestCase):
    """
    Test edge cases and error conditions.

    LEARNING NOTE: Edge case testing is crucial for embedded systems
    because they often operate in harsh environments with:
    - Power fluctuations
    - Temperature extremes
    - Electromagnetic interference
    - Component aging
    """

    @patch('src.sensors.dht11.dht.DHT11')
    @patch('src.sensors.dht11.Pin')
    def test_rapid_successive_readings(self, mock_pin, mock_dht11):
        """Test rate limiting prevents too-frequent readings."""
        # Set up mock DHT device
        mock_dht_device = MagicMock()
        mock_dht_device.temperature.return_value = 25.0
        mock_dht_device.humidity.return_value = 60.0
        mock_dht11.return_value = mock_dht_device

        # Initialize sensor with 0.5 Hz rate (2 second minimum interval)
        sensor = DHT11Sensor("Test DHT11", pin_number=17, sample_rate=0.5)
        sensor.initialize()

        # First reading should work
        reading1 = sensor.read()
        self.assertIsNotNone(reading1)

        # Immediate second reading should return cached result
        reading2 = sensor.read()
        self.assertEqual(reading1, reading2)  # Should be same object

        # Verify measure() was only called once (rate limited)
        self.assertEqual(mock_dht_device.measure.call_count, 1)

"""
LEARNING EXERCISES FOR TESTING:

1. RUN THE TESTS (BEGINNER):
   - Execute these tests using: python -m pytest tests/unit/test_dht11.py
   - Observe which tests pass and which fail
   - Understand how mocking allows testing without hardware

2. IMPLEMENT VALIDATION TESTING (INTERMEDIATE):
   - Add test cases for the _validate_reading() method you'll implement
   - Test boundary conditions (exactly 0°C, exactly 50°C, etc.)
   - Test invalid data handling

3. ADD COMFORT ANALYSIS TESTS (INTERMEDIATE):
   - Create tests for the get_comfort_status() method
   - Test different combinations of temperature and humidity
   - Verify recommendations are appropriate

4. INTEGRATION TESTING (ADVANCED):
   - Create tests that verify sensor works with actual automation logic
   - Test error recovery scenarios
   - Simulate long-running operation with periodic failures

5. PERFORMANCE TESTING (ADVANCED):
   - Test memory usage over extended operation
   - Verify timing constraints are met
   - Test behavior under high system load

TESTING CONCEPTS LEARNED:
- Unit testing with mocks for hardware independence
- Edge case identification and testing
- Error condition simulation
- Test data setup and teardown
- Assertion strategies for floating-point comparisons
- Rate limiting verification

PROFESSIONAL INSIGHT:
In embedded systems, thorough testing is critical because fixing bugs
after deployment often requires physical access to devices. These tests
help catch issues early and ensure reliability in production environments.
"""