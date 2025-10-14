from sensors.rfid import RFIDSensor
import time

sensor = RFIDSensor()
test_score = 0
get_card_id_result = False

print("="*50)
print("Testing RFID Sensor")
print("="*50)
print("\n⚠️  USER ACTION REQUIRED:")
print("   Scan an RFID card during the test")
print("   Test will wait 2 seconds between scans")
print("   You have 5 attempts to scan a card\n")

print("Testing scan_card (5 attempts)")
for i in range(5):
    result = sensor.scan_card()
    if result:
        card_id = sensor.get_card_id()
        print(f"  {i+1}. ✓ Card detected - ID: {card_id}")
        test_score += 1
    else:
        print(f"  {i+1}. No card detected")
    time.sleep(2)

print("\nTesting get_card_id")
result = sensor.get_card_id()
print(f"  Result: {result}")
if result is not None:
    get_card_id_result = True
    test_score += 1

print("\nTesting clear_card")
sensor.clear_card()
print("  Card cleared")
test_score += 1

print("\n" + "="*50)
print(f"Test Score: {test_score}/6")
if test_score >= 1 and get_card_id_result:
    print(f"✓ Test PASSED (card detected {test_score} times)")
else:
    print("✗ Test FAILED (no cards detected or no card ID returned)")
print("="*50)