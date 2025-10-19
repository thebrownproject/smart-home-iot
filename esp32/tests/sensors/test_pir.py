from sensors.pir import PIRSensor
import time

sensor = PIRSensor()
test_score = 0

print("="*50)
print("Testing PIR Sensor")
print("="*50)

print("\nTesting is_motion_detected")
result = sensor.is_motion_detected()
for i in range(5):
    result = sensor.is_motion_detected()
    print(f"  {i+1}. {result}")
    if result:
        test_score += 1
    time.sleep(2)

print("="*50)
print("Testing completed")
print(f"Test Score: {test_score}/5")
print("="*50)