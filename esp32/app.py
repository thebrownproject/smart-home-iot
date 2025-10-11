import time

class SmartHomeApp:
    def __init__(self, system):
        # Store Memory reference
        self.memory = system.memory

        # Create persistent MQTT connection (can't be deleted)
        from comms.mqtt_client import SmartHomeMQTTClient
        self.mqtt = SmartHomeMQTTClient()
        self.mqtt.connect()
        self.memory.collect("After MQTT setup")

    def run(self):
        from handlers.motion import MotionHandler
        from handlers.lighting import LightingHandler

        motion = MotionHandler()
        lighting = LightingHandler()
        
        print("App running...")
        loop_count = 0
        while True:
            # Check time-based lighting every 60 seconds (1 minute)
            if loop_count % 60 == 0:
                lighting.handle_time_based_lighting()

            # Check motion every 5 seconds
            if loop_count % 5 == 0:
                motion.handle_motion_detection(self.mqtt)

            # Garbage collection every 10 seconds
            if loop_count % 10 == 0:
                self.memory.collect("App loop")

            loop_count += 1
            time.sleep(1)  # Loop runs every 1 second
    
    

    
    
                