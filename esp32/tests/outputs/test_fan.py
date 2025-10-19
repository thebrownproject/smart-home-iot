from outputs.fan import Fan
import time

fan = Fan()
test_score = 0

print("="*50)
print("Testing Fan")
print("="*50)

print("\nTesting on and off")
for i in range(3):
    print(f"Test no: {i+1}")
    time.sleep(1)
    fan.on()
    print(f"  Fan is running")
    time.sleep(1)
    fan.off()
    print(f"  Fan is stopped")
    time.sleep(1)

print("="*50)
print("Testing completed")
print("="*50)


