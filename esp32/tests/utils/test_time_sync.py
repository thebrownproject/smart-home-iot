from utils.time_sync import TimeSync

time_sync = TimeSync()

print("="*50)
print("Time Sync Test")
print("="*50)

time_sync.sync_time()
print(time_sync.get_local_time())
print(time_sync.is_nighttime())
print("="*50)
