from config import TIMEZONE_OFFSET_HOURS, NIGHT_START_HOUR, NIGHT_END_HOUR
import ntptime
import time
class TimeSync:
    def __init__(self):
        self.timezone_offset = TIMEZONE_OFFSET_HOURS * 3600
        self.night_start = NIGHT_START_HOUR
        self.night_end = NIGHT_END_HOUR
        self.last_sync = None

    def sync_time(self):
        try:
            ntptime.settime()
            self.last_sync = time.time()
            return True  # Success
        except Exception as e:
            print(f"Error synchronizing time: {e}")
            return False
    
    def get_local_time(self):
        utc_seconds = time.time()
        local_seconds = utc_seconds + self.timezone_offset
        return time.localtime(local_seconds)
    
    def is_nighttime(self):
        local_time = self.get_local_time()
        hour = local_time[3]
        return hour >= self.night_start or hour < self.night_end
    
    def get_iso_timestamp(self):
        local_time = self.get_local_time()
        return "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
          local_time[0], local_time[1], local_time[2],
          local_time[3], local_time[4], local_time[5]
      )