from display.oled import OLED
import time

print("Starting OLED test...")

# Initialize OLED
oled = OLED()
print("✓ OLED initialized")
time.sleep(1)

# Test 1: Show text on two lines
print("Test 1: Displaying 'Hello' / 'World'")
oled.show_text("Hello", "World")
time.sleep(3)

# Test 2: Show temperature and humidity
print("Test 2: Displaying temp/humidity")
oled.show_temp_humidity(20, 50)
time.sleep(3)

# Test 3: Clear display
print("Test 3: Clearing display")
oled.clear()
time.sleep(1)

print("✓ OLED test completed successfully!")