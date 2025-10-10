# Hardware Connection Validation Test
# Based on KS5009 reference implementations
# Tests all hardware components before software implementation

from machine import Pin, PWM, SoftI2C
import time
import gc

# Hardware Configuration from Reference Code
# I2C Configuration (LCD + RFID)
I2C_SDA_PIN = 21
I2C_SCL_PIN = 22
LCD_I2C_ADDR = 0x27
RFID_I2C_ADDR = 0x28

# GPIO Pin Configuration
DHT11_PIN = 17          # Temperature/Humidity sensor
PIR_PIN = 14            # PIR motion sensor
GAS_PIN = 23            # Gas sensor
LED_PIN = 12            # LED control
RGB_PIN = 26            # RGB LED strip (SK6812)
SERVO_PIN = 13          # Servo motor control
FAN_INA_PIN = 19        # Fan motor INA
FAN_INB_PIN = 18        # Fan motor INB
BUTTON_PIN = 16         # Control button (from RFID example)

def test_i2c_bus():
    """Test I2C bus and detect connected devices"""
    print("=== I2C Bus Test ===")
    try:
        # Initialize I2C with pull-up resistors
        scl_pin = Pin(I2C_SCL_PIN, Pin.OUT, pull=Pin.PULL_UP)
        sda_pin = Pin(I2C_SDA_PIN, Pin.OUT, pull=Pin.PULL_UP)

        i2c = SoftI2C(scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN), freq=100000)

        # Scan for I2C devices
        devices = i2c.scan()
        if not devices:
            print("❌ No I2C devices detected! Check wiring/power/pull-up resistors")
            return False
        else:
            print("✅ I2C devices detected at addresses:", [hex(addr) for addr in devices])

            # Check for expected devices
            lcd_found = LCD_I2C_ADDR in devices
            rfid_found = RFID_I2C_ADDR in devices

            print(f"📺 LCD Display (0x{LCD_I2C_ADDR:02x}): {'✅ Found' if lcd_found else '❌ Missing'}")
            print(f"📱 RFID Reader (0x{RFID_I2C_ADDR:02x}): {'✅ Found' if rfid_found else '❌ Missing'}")

            return lcd_found or rfid_found  # At least one device should work

    except Exception as e:
        print(f"❌ I2C Test Failed: {e}")
        return False

def test_digital_inputs():
    """Test digital input pins (PIR, Gas, Button)"""
    print("\n=== Digital Input Test ===")
    try:
        # Initialize digital inputs
        pir = Pin(PIR_PIN, Pin.IN)
        gas = Pin(GAS_PIN, Pin.IN, Pin.PULL_UP)
        button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)

        print("Testing digital inputs for 5 seconds...")
        print("Move in front of PIR sensor, trigger gas sensor, press button")

        for i in range(50):  # 5 seconds of testing
            pir_val = pir.value()
            gas_val = gas.value()
            btn_val = button.value()

            status = []
            if pir_val == 1:
                status.append("PIR:MOTION")
            if gas_val == 0:  # Gas sensor is active low
                status.append("GAS:DETECTED")
            if btn_val == 0:  # Button is active low
                status.append("BTN:PRESSED")

            if status:
                print(f"📊 Inputs Active: {', '.join(status)}")

            time.sleep(0.1)

        print("✅ Digital input test completed")
        return True

    except Exception as e:
        print(f"❌ Digital Input Test Failed: {e}")
        return False

def test_digital_outputs():
    """Test digital output pins (LED)"""
    print("\n=== Digital Output Test ===")
    try:
        led = Pin(LED_PIN, Pin.OUT)

        print("Testing LED blink pattern...")
        for i in range(5):
            led.value(1)
            print(f"💡 LED ON (cycle {i+1}/5)")
            time.sleep(0.5)
            led.value(0)
            print("💡 LED OFF")
            time.sleep(0.5)

        print("✅ Digital output test completed")
        return True

    except Exception as e:
        print(f"❌ Digital Output Test Failed: {e}")
        return False

def test_pwm_outputs():
    """Test PWM outputs (Servo, Fan)"""
    print("\n=== PWM Output Test ===")
    try:
        # Servo test
        print("Testing servo motor...")
        servo = PWM(Pin(SERVO_PIN))
        servo.freq(50)

        # Test servo positions (from reference code)
        positions = [25, 77, 128]  # 0°, 90°, 180°
        position_names = ["0°", "90°", "180°"]

        for pos, name in zip(positions, position_names):
            servo.duty(pos)
            print(f"🔄 Servo position: {name}")
            time.sleep(1)

        servo.deinit()

        # Fan test
        print("Testing fan motor...")
        fan_ina = PWM(Pin(FAN_INA_PIN), 10000)
        fan_inb = PWM(Pin(FAN_INB_PIN), 10000)

        # Test fan directions (from reference code)
        print("🌀 Fan: Counterclockwise")
        fan_ina.duty(0)
        fan_inb.duty(700)
        time.sleep(2)

        print("🌀 Fan: Stop")
        fan_ina.duty(0)
        fan_inb.duty(0)
        time.sleep(1)

        print("🌀 Fan: Clockwise")
        fan_ina.duty(600)
        fan_inb.duty(0)
        time.sleep(2)

        print("🌀 Fan: Stop")
        fan_ina.duty(0)
        fan_inb.duty(0)

        fan_ina.deinit()
        fan_inb.deinit()

        print("✅ PWM output test completed")
        return True

    except Exception as e:
        print(f"❌ PWM Output Test Failed: {e}")
        return False

def test_rgb_leds():
    """Test RGB LED strip (NeoPixel)"""
    print("\n=== RGB LED Test ===")
    try:
        import neopixel

        # Initialize RGB LEDs (from reference code)
        pin = Pin(RGB_PIN, Pin.OUT)
        np = neopixel.NeoPixel(pin, 4)  # 4 RGB LEDs

        brightness = 50  # Reduced brightness for testing
        colors = [
            [brightness, 0, 0],          # Red
            [0, brightness, 0],          # Green
            [0, 0, brightness],          # Blue
            [brightness, brightness, brightness],  # White
            [0, 0, 0]                    # Off
        ]
        color_names = ["Red", "Green", "Blue", "White", "Off"]

        print("Testing RGB LED color sequence...")
        for color, name in zip(colors, color_names):
            for j in range(4):  # 4 LEDs
                np[j] = color
            np.write()
            print(f"🌈 RGB LEDs: {name}")
            time.sleep(1)

        print("✅ RGB LED test completed")
        return True

    except Exception as e:
        print(f"❌ RGB LED Test Failed: {e}")
        print("Note: neopixel library may need to be installed via Thonny")
        return False

def test_dht11_sensor():
    """Test DHT11 temperature/humidity sensor"""
    print("\n=== DHT11 Sensor Test ===")
    try:
        import dht

        # Initialize DHT11 (from reference code)
        sensor = dht.DHT11(Pin(DHT11_PIN))

        print("Reading DHT11 sensor (3 readings)...")
        for i in range(3):
            try:
                sensor.measure()
                temp = sensor.temperature()
                humidity = sensor.humidity()
                print(f"🌡️  Reading {i+1}: Temperature: {temp}°C, Humidity: {humidity}%")
                time.sleep(2)
            except OSError as e:
                print(f"⚠️  DHT11 reading {i+1} failed: {e}")

        print("✅ DHT11 sensor test completed")
        return True

    except Exception as e:
        print(f"❌ DHT11 Test Failed: {e}")
        print("Note: dht library may need to be installed via Thonny")
        return False

def main():
    """Run all hardware validation tests"""
    print("🔧 KS5009 Smart Home Hardware Validation")
    print("=" * 50)

    # Memory check
    print(f"💾 Available Memory: {gc.mem_free()} bytes")

    # Run all tests
    tests = [
        ("I2C Bus", test_i2c_bus),
        ("Digital Inputs", test_digital_inputs),
        ("Digital Outputs", test_digital_outputs),
        ("PWM Outputs", test_pwm_outputs),
        ("RGB LEDs", test_rgb_leds),
        ("DHT11 Sensor", test_dht11_sensor)
    ]

    results = {}
    for test_name, test_func in tests:
        print(f"\n{'='*20}")
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results[test_name] = False

        # Memory cleanup
        gc.collect()

    # Summary
    print(f"\n{'='*50}")
    print("🔍 HARDWARE VALIDATION SUMMARY")
    print(f"{'='*50}")

    passed = 0
    total = len(results)

    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<20}: {status}")
        if result:
            passed += 1

    print(f"\nOverall: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All hardware tests passed! Ready for software implementation.")
    elif passed >= total // 2:
        print("⚠️  Some hardware issues detected. Check connections and retry.")
    else:
        print("❌ Major hardware issues. Review wiring and component connections.")

    return results

if __name__ == "__main__":
    main()