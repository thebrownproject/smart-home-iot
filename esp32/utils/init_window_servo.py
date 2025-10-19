"""
Window Servo Calibration Script

⚠️  DEVELOPMENT TOOL - NOT USED IN MAIN APPLICATION

Purpose:
    Manual testing script to calibrate the window servo (pin 5).
    Tests servo movement between 0°, 90°, and back to 0°.

Usage:
    1. Upload to ESP32 via MicroPico
    2. Run directly in REPL to test servo
    3. Adjust angle values if servo doesn't reach correct positions

Duty cycle to angle mapping:
    0°   = 2.5%  = 25
    45°  = 5%    = 51.2
    90°  = 7.5%  = 77
    135° = 10%   = 102.4
    180° = 12.5% = 128

These calibrated values are used in outputs/servo.py
"""
from machine import Pin, PWM
import time
pwm = PWM(Pin(5))
pwm.freq(50)
angle_0 = 25
angle_90 = 77
angle_180 = 128

pwm.duty(angle_0)
time.sleep(1)
pwm.duty(angle_90)
time.sleep(1)
pwm.duty(angle_0)
time.sleep(1)

# while True: