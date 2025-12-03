from comms.supabase import Supabase

supabase = Supabase()

print("="*50)
print("Supabase Test")
print("="*50)

print("\nTesting insert_sensor_log")
result = supabase.insert_sensor_log("temperature", 25, "°C")
print(f"  Result: {result}")

print("\nTesting insert_rfid_scan")
result = supabase.insert_rfid_scan("1234567890", "granted", 1)
print(f"  Result: {result}")

print("\nTesting insert_motion_event")
result = supabase.insert_motion_event()
print(f"  Result: {result}")