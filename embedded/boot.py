# boot.py - ESP32 Boot Configuration
# This file runs automatically when the ESP32 starts up

import gc
import machine
import time

print("Smart Home System - Boot Sequence Starting...")

# Enable garbage collection for memory management
gc.collect()

# Configure system-level settings
print("System Memory:", gc.mem_free(), "bytes free")

# Boot sequence complete - main.py will run next
print("Boot sequence complete - transferring to main.py")