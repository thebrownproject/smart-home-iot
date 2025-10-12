from handlers.lighting_handler import LightingHandler
import time

lighting_handler = LightingHandler()

print("="*50)
print("Testing Lighting Handler")
print("="*50)

for i in range(3):
    print(f"Test {i+1}")
    lighting_handler.handle_time_based_lighting()
    time.sleep(1)

print("="*50)
print("Testing completed")
print("="*50)