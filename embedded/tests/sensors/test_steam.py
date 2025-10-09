from sensors.steam import SteamSensor
import time

sensor = SteamSensor()
test_score = 0

print("="*50)
print("Testing Steam Sensor")
print("="*50)

print("\nTesting read")
for i in range(5):
    result = sensor.read()
    print(f"  {i+1}. {result}")
    time.sleep(2)

print("\nTesting is_moisture_detected")
result = sensor.is_moisture_detected()
print(f"  Result: {result}")

print("="*50)
print("Testing completed")
print("="*50)