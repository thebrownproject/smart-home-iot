import time
from utils.memory import Memory

class SmartHomeApp:
    def __init__(self):
        self.memory = Memory()
        from config import TOPIC_RFID_RESPONSE, TOPIC_CONTROL_DOOR, TOPIC_CONTROL_WINDOW, TOPIC_CONTROL_FAN, TOPIC_REQUEST_STATUS
        from handlers.control_handler import ControlHandler
        from outputs.rgb import RGBManager
        from outputs.oled import OLEDManager
        from outputs.servo import DoorServoManager
        from outputs.servo import WindowServoManager
        from outputs.buzzer import BuzzerManager
        from outputs.fan import FanManager

        self.rgb_manager = RGBManager()
        self.oled_manager = OLEDManager()
        self.door_servo_manager = DoorServoManager()
        self.window_servo_manager = WindowServoManager()
        self.buzzer_manager = BuzzerManager()
        self.fan_manager = FanManager()

        # Create environment handler early for status requests
        from handlers.environment_handler import EnvironmentHandler
        self.environment = EnvironmentHandler()

        from outputs.oled import OLED
        oled = OLED()
        oled.show_text("MQTT Broker", "Connecting...")

        # Create persistent MQTT connection (can't be deleted)
        from comms.mqtt_client import SmartHomeMQTTClient
        self.mqtt = SmartHomeMQTTClient()

        max_retries = 3
        for attempt in range(max_retries):
            if self.mqtt.connect():
                oled.show_text("MQTT Broker", "Connected")
                time.sleep(1)
                break
            else:
                print(f"MQTT connection attempt {attempt + 1}/{max_retries} failed")
                if attempt < max_retries - 1:
                    oled.show_text("MQTT Retry", f"Attempt {attempt + 2}/{max_retries}")
                    time.sleep(2)
                else:
                    oled.show_text("MQTT FAILED", "System halted")
                    time.sleep(3)
                    raise RuntimeError("MQTT connection failed after all retries - system cannot operate without broker")

        # Give door servo manager access to MQTT for auto-close status updates
        self.door_servo_manager.set_mqtt(self.mqtt)

        self.control = ControlHandler(self.rgb_manager, self.oled_manager, self.door_servo_manager, self.window_servo_manager, self.buzzer_manager, self.fan_manager)
        # Give control handler access to MQTT for publishing door status on RFID access
        self.control.set_mqtt(self.mqtt)

        # Subscribe to MQTT topics with control handler methods as callbacks
        self.mqtt.subscribe(TOPIC_RFID_RESPONSE, self.control.handle_rfid_response)
        self.mqtt.subscribe(TOPIC_CONTROL_DOOR, lambda t, m: self.control.handle_door_control(t, m, self.mqtt))
        self.mqtt.subscribe(TOPIC_CONTROL_WINDOW, lambda t, m: self.control.handle_window_control(t, m, self.mqtt))
        self.mqtt.subscribe(TOPIC_CONTROL_FAN, lambda t, m: self.control.handle_fan_control(t, m, self.mqtt))
        self.mqtt.subscribe(TOPIC_REQUEST_STATUS, lambda t, m: self.control.handle_status_request(t, m, self.mqtt, self.environment))
        self.memory.collect("After MQTT setup")
        oled.show_text("System Ready", "App Running")
        del oled

    def run(self):
        from handlers.motion_handler import MotionHandler
        from handlers.lighting_handler import LightingHandler
        from handlers.steam_handler import SteamHandler
        from handlers.gas_handler import GasHandler
        from handlers.rfid_handler import RFIDHandler
        from handlers.button_handler import ButtonHandler

        motion = MotionHandler()
        lighting = LightingHandler()
        steam = SteamHandler()
        gas = GasHandler()
        rfid = RFIDHandler()
        button = ButtonHandler()

        print("App running...")
        loop_count = 1  # Start at 1 to avoid startup spike (0 % n == 0 for all n)
        while True:
            self.rgb_manager.update()
            self.oled_manager.update()
            self.door_servo_manager.update()
            self.window_servo_manager.update()
            self.buzzer_manager.update()
            self.fan_manager.update()
            self.mqtt.check_messages()

            button.handle_buttons(self.oled_manager)

            if loop_count % 60 == 0:
                lighting.handle_time_based_lighting()

            if loop_count % 2 == 0:
                motion.handle_motion_detection(self.mqtt, self.rgb_manager, self.oled_manager, button)

            if loop_count % 10 == 0:
                steam.handle_steam_detection(self.mqtt, self.rgb_manager, self.oled_manager, self.window_servo_manager)

            if loop_count % 10 == 5:
                gas.handle_gas_detection(self.mqtt, self.rgb_manager, self.oled_manager, self.buzzer_manager, button, self.fan_manager)

            rfid.handle_rfid_detection(self.mqtt, self.oled_manager)

            self.environment.handle_environment_detection(self.mqtt, self.oled_manager)

            if loop_count % 10 == 1:
                self.memory.collect("App loop")

            loop_count += 1
            print(f"--- Loop {loop_count} complete ---")
            time.sleep(1)  # Loop runs every 1 second