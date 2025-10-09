from outputs.rgb import RGB
import time

rgb = RGB()

print("="*50)
print("Testing RGB LED")
print("="*50)

print("\nTest 1: Solid colors (FR2.2, FR4.3)")
print("  Setting RED (gas alert)")
rgb.set_color(255, 0, 0)
time.sleep(2)

print("  Setting ORANGE (motion detection)")
rgb.set_color(255, 165, 0)
time.sleep(2)

print("  Setting OFF")
rgb.off()
time.sleep(1)

print("\nTest 2: Flashing colors (FR3.3, FR5.2)")
print("  Flashing BLUE 3 times (steam detection)")
rgb.flash((0, 0, 255), 3)

print("  Flashing RED 3 times (RFID denied)")
rgb.flash((255, 0, 0), 3)

print("\n" + "="*50)
print("Testing completed")
print("Verify visually: Did RGB show red, orange, blue?")
print("="*50)
