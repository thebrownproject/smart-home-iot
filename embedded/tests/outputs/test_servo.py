from outputs.servo import Servo
import time

door_servo = Servo(13)
window_servo = Servo(5)
test_score = 0

print("="*50)
print("Testing Servo")
print("="*50)

print("\nTesting open and close")
for i in range(3):
    print(f"Test no: {i+1}")
    time.sleep(1)
    door_servo.open()
    print(f"  Door servo is open ")
    time.sleep(1)
    door_servo.close()
    print(f"  Door servo is closed")
    time.sleep(1)

print("\nTesting window open and close")
for i in range(3):
    print(f"Test no: {i+1}")
    time.sleep(1)
    window_servo.open()
    print(f"  Window servo is open")
    time.sleep(1)
    window_servo.close()
    print(f"  Window servo is closed")
    time.sleep(1)

print("="*50)
print("Testing completed")
print("="*50)