from sensors.gas import GasSensor
import time

sensor = GasSensor()
test_score = 0

print("="*50)
print("Testing Gas Sensor")
print("="*50)

print("Testing read_value (5 readings)")
for i in range(5):
    result = sensor.read_value()
    assert result in [0, 1], f"Invalid reading: {result} (expected 0 or 1)"
    if result == 0:
        print(f"  {i+1}. Result: {result} - GAS DETECTED ⚠️")
    else:
        print(f"  {i+1}. Result: {result} - No gas (normal)")
    test_score += 1
    time.sleep(2)

print("\nTesting is_gas_detected")
result = sensor.is_gas_detected()
if result:
    print(f"  Result: {result} - GAS DETECTED ⚠️")
else:
    print(f"  Result: {result} - No gas (normal)")
test_score += 1

print("\n" + "="*50)
print(f"Test Score: {test_score}/6")
if test_score == 6:
    print("✓ Test PASSED (all readings valid)")
else:
    print(f"✗ Test FAILED ({6-test_score} invalid readings)")
print("="*50)