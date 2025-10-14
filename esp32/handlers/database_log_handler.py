from utils.memory import Memory

class DatabaseLogHandler:
    def __init__(self):
        self.memory = Memory()

    def handle_database_log(self):
        """Log temperature and humidity to database every 30 minutes (FR6.4)"""
        from sensors.dht11 import DHT11
        from comms.supabase.sensor_logs import insert_sensor_log
        import gc

        dht11 = DHT11(17)
        temp, humidity = dht11.read_data()

        if temp is not None and humidity is not None:
            insert_sensor_log("temperature", temp, "C")
            insert_sensor_log("humidity", humidity, "%")
            print(f"DatabaseLogHandler - Logged: Temp={temp}C, Humidity={humidity}%")
        else:
            print("DatabaseLogHandler - Sensor read failed, skipping log")

        del dht11, insert_sensor_log
        gc.collect()
        self.memory.collect("After database log")
