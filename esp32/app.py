import time
from utils.memory import Memory

class SmartHomeApp:
    def __init__(self):
        # Store Memory reference
        self.memory = Memory()

        # Create persistent MQTT connection (can't be deleted)
        from comms.mqtt_client import SmartHomeMQTTClient
        self.mqtt = SmartHomeMQTTClient()
        self.mqtt.connect()
        self.memory.collect("After MQTT setup")

    def run(self):
        from handlers.motion_handler import MotionHandler
        from handlers.lighting_handler import LightingHandler
        from handlers.steam_handler import SteamHandler
        from handlers.gas_handler import GasHandler
        from handlers.rfid_handler import RFIDHandler
        from handlers.enviroment_handler import EnvironmentHandler
        from handlers.database_log_handler import DatabaseLogHandler

        motion = MotionHandler()
        lighting = LightingHandler()
        steam = SteamHandler()
        gas = GasHandler()
        rfid = RFIDHandler()
        environment = EnvironmentHandler()
        database_logger = DatabaseLogHandler()

        print("App running...")
        loop_count = 0
        while True:
            # Check time-based lighting every 60 seconds (1 minute)
            if loop_count % 60 == 0:
                lighting.handle_time_based_lighting()

            # Check motion every 5 seconds
            if loop_count % 5 == 0:
                motion.handle_motion_detection(self.mqtt)

            # Check steam every 10 seconds
            if loop_count % 10 == 0:
                steam.handle_steam_detection(self.mqtt)

            # Check gas every 10 seconds
            if loop_count % 10 == 0:
                gas.handle_gas_detection(self.mqtt)

            # Check RFID every 2 seconds
            if loop_count % 2 == 0:
                rfid.handle_rfid_detection(self.mqtt)

            # Check environment (temp/humidity) every 2 seconds
            if loop_count % 2 == 0:
                environment.handle_environment_detection(self.mqtt)

            # Log sensor data to database every 30 minutes (1800 seconds) - FR6.4
            if loop_count % 1800 == 0:
                database_logger.handle_database_log()

            # Garbage collection every 10 seconds
            if loop_count % 10 == 0:
                self.memory.collect("App loop")

            loop_count += 1
            time.sleep(1)  # Loop runs every 1 second
    
    

    
    
                