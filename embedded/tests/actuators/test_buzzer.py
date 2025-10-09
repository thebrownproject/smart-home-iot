from actuators.buzzer import Buzzer
import time

buzzer = Buzzer()

print("="*50)
print("Testing Buzzer")
print("="*50)

print("\nTest 1: Single beeps (default duration)")
for i in range(3):
    print(f"  Beep {i+1}")
    buzzer.beep()
    time.sleep(0.5)  # Pause between beeps

print("\nTest 2: Short beeps")
for i in range(3):
    print(f"  Short beep {i+1}")
    buzzer.beep(0.1)  # 0.1 second beep
    time.sleep(0.3)

print("\nTest 3: Long beep")
print("  Long beep")
buzzer.beep(1.0)  # 1 second beep
time.sleep(0.5)

print("\nTest 4: Pattern (3 beeps)")
print("  Playing pattern...")
buzzer.pattern(3, 0.2)  # 3 beeps with 0.2s interval

print("\n" + "="*50)
print("Testing completed")
print("="*50)
