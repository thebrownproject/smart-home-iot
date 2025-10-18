import time
from utils.memory import Memory

class SmartHomeApp:
    def __init__(self):
        # Store Memory reference
        self.memory = Memory()
        from config import TOPIC_RFID_RESPONSE, TOPIC_CONTROL_DOOR, TOPIC_CONTROL_WINDOW, TOPIC_CONTROL_FAN
        from handlers.control_handler import ControlHandler
        from outputs.rgb import RGBManager
        from display.oled import OLEDManager
        from outputs.servo import DoorServoManager

        # Create RGB manager (shared across all handlers)
        self.rgb_manager = RGBManager()
        self.oled_manager = OLEDManager()
        self.door_servo_manager = DoorServoManager()

        # Show MQTT connecting status
        from display.oled import OLED
        oled = OLED()
        oled.show_text("MQTT Broker", "Connecting...")

        # Create persistent MQTT connection (can't be deleted)
        from comms.mqtt_client import SmartHomeMQTTClient
        self.mqtt = SmartHomeMQTTClient()
        self.mqtt.connect()

        # Create control handler with manager references
        self.control = ControlHandler(self.rgb_manager, self.oled_manager, self.door_servo_manager)
        
        # Subscribe to MQTT topics with control handler methods as callbacks
        self.mqtt.subscribe(TOPIC_RFID_RESPONSE, self.control.handle_rfid_response)
        self.mqtt.subscribe(TOPIC_CONTROL_DOOR, self.control.handle_door_control)
        self.mqtt.subscribe(TOPIC_CONTROL_WINDOW, self.control.handle_window_control)
        self.mqtt.subscribe(TOPIC_CONTROL_FAN, self.control.handle_fan_control)
        self.memory.collect("After MQTT setup")

        # Show connection success
        oled.show_text("MQTT Broker", "Connected")
        time.sleep(2)
        oled.show_text("System Ready", "App Running")
        del oled

    def run(self):
        from handlers.motion_handler import MotionHandler
        from handlers.lighting_handler import LightingHandler
        from handlers.steam_handler import SteamHandler
        from handlers.gas_handler import GasHandler
        from handlers.rfid_handler import RFIDHandler
        from handlers.environment_handler import EnvironmentHandler

        motion = MotionHandler()
        lighting = LightingHandler()
        steam = SteamHandler()
        gas = GasHandler()
        rfid = RFIDHandler()
        environment = EnvironmentHandler()

        print("App running...")
        loop_count = 1  # Start at 1 to avoid startup spike (0 % n == 0 for all n)
        while True:
            self.rgb_manager.update()
            self.oled_manager.update()
            self.door_servo_manager.update()
            self.mqtt.check_messages()

            # Check time-based lighting every 60 seconds (1 minute)
            if loop_count % 60 == 0:
                lighting.handle_time_based_lighting()

            # Check motion every 2 seconds (responsive to quick movements)
            if loop_count % 2 == 0:
                motion.handle_motion_detection(self.mqtt, self.rgb_manager, self.oled_manager)

            # Check steam every 10 seconds (staggered at loop 10, 20, 30...)
            if loop_count % 10 == 0:
                steam.handle_steam_detection(self.mqtt, self.rgb_manager, self.oled_manager)

            # Check gas every 10 seconds (staggered at loop 5, 15, 25... to avoid loop 10 collision)
            if loop_count % 10 == 5:
                gas.handle_gas_detection(self.mqtt, self.rgb_manager, self.oled_manager)

            # Check RFID every 3 seconds (offset from environment to reduce collisions)
            if loop_count % 3 == 0:
                rfid.handle_rfid_detection(self.mqtt, self.oled_manager)

            # Check environment every loop (acts as fallback display - no flicker due to idle detection)
            environment.handle_environment_detection(self.mqtt, self.oled_manager)

            # Garbage collection every 10 seconds (run AFTER handlers complete, at loop 1, 11, 21...)
            if loop_count % 10 == 1:
                self.memory.collect("App loop")

            loop_count += 1
            print(f"--- Loop {loop_count} complete ---")
            time.sleep(1)  # Loop runs every 1 second