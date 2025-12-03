from sensors.steam import SteamSensor
import time

sensor = SteamSensor()
test_score = 0

print("="*50)
print("Testing Steam Sensor")
print("="*50)

print("\nTesting is_moisture_detected")
for i in range(5):
    result = sensor.is_moisture_detected()
    print(f"  Result: {result}")
    if result:
        test_score += 1
    time.sleep(2)

print("="*50)
print(f"Test Score: {test_score}/5")
if test_score == 5:
    print("✓ Test PASSED")
else:
    print(f"✗ Test FAILED ({5-test_score} errors)")
print("="*50)