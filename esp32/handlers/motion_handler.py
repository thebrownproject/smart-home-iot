from utils.memory import Memory


class MotionHandler:

    def __init__(self):
        self.memory = Memory()
        self.motion_count = 0
        
    def handle_motion_detection(self, mqtt):
            """Check PIR and respond to motion (FR2.1, FR2.2, FR2.3)"""
            from sensors.pir import PIRSensor
            from outputs.rgb import RGB

            pir = PIRSensor()
            rgb = RGB()

            if pir.is_motion_detected():
                self.memory.collect("MotionHandler - Motion detected")
                self.motion_count = 3

                # Set RGB to orange (FR2.2)
                rgb.set_color(255, 165, 0)  # Orange

                # MQTT publish (uses persistent connection)
                if mqtt.publish("home/motion", '{"detected": true}'):
                    print("MotionHandler - MQTT Publish OK")

                self.memory.collect("Before DB insert")

                # Supabase insert
                try:
                    from comms.supabase.motion_events import insert_motion_event
                    insert_motion_event()
                    print("MotionHandler - DB Insert OK")
                    del insert_motion_event
                except Exception as e:
                    print(f"MotionHandler - DB Insert ERROR: {e}")

                self.memory.collect("After motion handling")
            # Don't turn off RGB - let state machine handle priority (T1.29)
            if self.motion_count > 0:  # Only count down if timer active
                self.motion_count -= 1
                if self.motion_count == 0:  # Turn off when timer expires
                    rgb.off()
            del pir, rgb
            self.memory.collect("After motion check")