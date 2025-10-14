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
    assert fan.ina.duty() == 0 and fan.inb.duty() == 700
    print(f"  Fan is running: {fan.is_running()}")
    time.sleep(1)
    fan.off()
    assert fan.ina.duty() == 0 and fan.inb.duty() == 0
    print(f"  Fan is running: {fan.is_running()}")
    time.sleep(1)

print("="*50)
print("Testing completed")
print("="*50)


