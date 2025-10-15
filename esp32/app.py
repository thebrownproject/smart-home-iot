import time
from utils.memory import Memory

class SmartHomeApp:
    def __init__(self):
        # Store Memory reference
        self.memory = Memory()
        from config import TOPIC_RFID_RESPONSE, TOPIC_CONTROL_DOOR, TOPIC_CONTROL_WINDOW, TOPIC_CONTROL_FAN
        from handlers.control_handler import ControlHandler

        # Create persistent MQTT connection (can't be deleted)
        from comms.mqtt_client import SmartHomeMQTTClient
        self.mqtt = SmartHomeMQTTClient()
        self.mqtt.connect()

        # Create control handler for MQTT callbacks
        self.control = ControlHandler()

        # Subscribe to MQTT topics with control handler methods as callbacks
        self.mqtt.subscribe(TOPIC_RFID_RESPONSE, self.control.handle_rfid_response)
        self.mqtt.subscribe(TOPIC_CONTROL_DOOR, self.control.handle_door_control)
        self.mqtt.subscribe(TOPIC_CONTROL_WINDOW, self.control.handle_window_control)
        self.mqtt.subscribe(TOPIC_CONTROL_FAN, self.control.handle_fan_control)
        self.memory.collect("After MQTT setup")

    def run(self):
        from handlers.motion_handler import MotionHandler
        from handlers.lighting_handler import LightingHandler
        from handlers.steam_handler import SteamHandler
        from handlers.gas_handler import GasHandler
        from handlers.rfid_handler import RFIDHandler
        from handlers.enviroment_handler import EnvironmentHandler

        motion = MotionHandler()
        lighting = LightingHandler()
        steam = SteamHandler()
        gas = GasHandler()
        rfid = RFIDHandler()
        environment = EnvironmentHandler()

        print("App running...")
        loop_count = 0
        while True:
            self.mqtt.check_messages()
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

            # Garbage collection every 10 seconds
            if loop_count % 10 == 0:
                self.memory.collect("App loop")

            loop_count += 1
            print(f"--- Loop {loop_count} complete ---")
            time.sleep(1)  # Loop runs every 1 second

    
    
    

    
    
                