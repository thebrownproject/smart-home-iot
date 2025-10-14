from utils.memory import Memory
from sensors.rfid import RFIDSensor
from outputs.buzzer import Buzzer

class RFIDHandler:
    def __init__(self):
        self.memory = Memory()
        self.rfid = RFIDSensor()  # Initialize once, reuse across calls
        self.buzzer = Buzzer()

    def handle_rfid_detection(self, mqtt):
        from outputs.rgb import RGB
        from outputs.servo import Servo
        from display.oled import OLED
        from comms.supabase.rfid_results import get_card_result
        from comms.supabase.rfid_scans import insert_rfid_scan
        rgb = RGB()
        door_servo = Servo(pin=13)
        oled = OLED()

        self.memory.collect("Before RFID handling")
        self.buzzer.stop()
        rgb.off()

        print("starting rfid test")

        if self.rfid.scan_card():
            card_id = self.rfid.get_card_id()
            print(f"DEBUG: Card scanned, ID: {card_id}")

            if not card_id:
                print("DEBUG: No card ID, exiting handler")
                del rgb, door_servo, oled
                self.memory.collect("After RFID handling")
                return

            card_record = get_card_result(card_id)
            print(f"DEBUG: Card record from DB: {card_record}")
            if card_record:
                rgb.set_color(0, 255, 0)
                door_servo.open()
                oled.show_text("ACCESS GRANTED", "Welcome home")
                payload = '{"card_id": "' + card_id + '", "access": "granted"}'
                if mqtt.publish("home/rfid", payload):
                    print("RFIDHandler - MQTT Publish OK")
                insert_rfid_scan(card_id, "granted", card_record['id'])
            else:
                print("DEBUG: Access denied - buzzer is COMMENTED OUT")
                rgb.set_color(255, 0, 0)
                self.buzzer.start()
                oled.show_text("ACCESS DENIED", "Unauthorised access")
                payload = '{"card_id": "' + card_id + '", "access": "denied"}'
                door_servo.close()
                if mqtt.publish("home/rfid", payload):
                    print("RFIDHandler - MQTT Publish OK")
                insert_rfid_scan(card_id, "denied", None)
            self.rfid.clear_card()
        del rgb, get_card_result, insert_rfid_scan, door_servo, oled
        self.memory.collect("After RFID handling")