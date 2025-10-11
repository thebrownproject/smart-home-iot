from utils.memory import Memory

class MotionHandler:

    def __init__(self):
        self.memory = Memory()
        
    def handle_motion_detection(self, mqtt):
            """Check PIR and respond to motion (FR2.1, FR2.2, FR2.3)"""
            from sensors.pir import PIRSensor
            from outputs.rgb import RGB

            pir = PIRSensor()
            rgb = RGB()

            if pir.is_motion_detected():
                rgb.set_color(255, 165, 0)  # Orange color (FR2.2)
                self.memory.collect("Motion detected")

                # MQTT publish (uses persistent connection)
                if mqtt.publish("home/motion", '{"detected": true}'):
                    print("Motion - MQTT OK")

                self.memory.collect("Before DB insert")

                # Supabase insert
                try:
                    from comms.supabase import Supabase
                    supabase = Supabase()
                    if supabase.insert_motion_event():
                        print("Motion - DB OK")
                    else:
                        print("Motion - DB FAILED")
                    del supabase
                except Exception as e:
                    print(f"Motion - DB ERROR: {e}")

                self.memory.collect("After motion handling")
            else:
                rgb.off()

            del pir, rgb
            self.memory.collect("After motion check")