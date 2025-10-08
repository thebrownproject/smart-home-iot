#!/usr/bin/env python3
"""
ESP32 Deployment Script
Uploads embedded/ directory to ESP32 using mpremote
"""

import os
import sys

def deploy():
    """Deploy embedded code to ESP32 via mpremote"""
    print("=" * 60)
    print("ESP32 Smart Home - Deployment Script")
    print("=" * 60)
    print("\nDeploying embedded/ directory to ESP32...")
    print("Target device: /dev/tty.usbserial-10")
    print()

    try:
        # Use mpremote to copy embedded directory contents to ESP32 root
        # The ':' destination means ESP32 root directory
        result = os.system("mpremote connect /dev/tty.usbserial-10 cp -r embedded/* :")

        if result == 0:
            print("\n" + "=" * 60)
            print("✅ Deployment complete!")
            print("=" * 60)
            print("\nNext steps:")
            print("1. Reset the ESP32 (press reset button or power cycle)")
            print("2. boot.py will run automatically")
            print("3. Then main.py will execute")
            print("\nTo see ESP32 output:")
            print("  mpremote connect /dev/tty.usbserial-10 repl")
            print()
            return 0
        else:
            print("\n" + "=" * 60)
            print("❌ Deployment failed!")
            print("=" * 60)
            print("\nTroubleshooting:")
            print("1. Check ESP32 is connected via USB")
            print("2. Verify device path: ls /dev/tty.usb*")
            print("3. Try: mpremote connect list")
            print("4. Check permissions: sudo chmod 666 /dev/tty.usbserial-10")
            print()
            return 1

    except Exception as e:
        print(f"\n❌ Error during deployment: {e}")
        print("\nMake sure mpremote is installed:")
        print("  pip install mpremote")
        return 1

if __name__ == "__main__":
    sys.exit(deploy())
