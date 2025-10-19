from outputs.led import LED


led = LED()
test_score = 0

print("="*50)
print("Testing LED")
print("="*50)


for i in range(3):
    print(f"Test no: {i+1}")
    print(f"  LED on")
    led.on()
    time.sleep(1)
    print(f"  LED off")
    led.off()
    time.sleep(1)

print("="*50)
print("Testing completed")
print("="*50)