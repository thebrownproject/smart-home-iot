from sensors.dht11 import DHT11Sensor
import time

sensor = DHT11Sensor()
test_score = 0

print("="*50)
print("Testing DHT11 Sensor")
print("="*50)

print("\nTesting read_data")
for i in range(5):
    result = sensor.read_data()
    print(f"  {i+1}. {result}")
    if result != (None, None):
        test_score += 1
    time.sleep(2)

print("\n" + "="*50)
print(f"Test Score: {test_score}/5")
if test_score == 5:
    print("✓ Test PASSED")
else:
    print(f"✗ Test FAILED ({5-test_score} errors)")
print("="*50)