from comms.supabase import Supabase

supabase = Supabase()

print("="*50)
print("Supabase Test")
print("="*50)

print("\nTesting insert_sensor_log")
result = supabase.insert_sensor_log("temperature", 25, "°C")
print(f"  Result: {result}")