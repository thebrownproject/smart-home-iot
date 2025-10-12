from utils.memory import Memory

class RFIDHandler:
    def __init__(self):
        self.memory = Memory()

    def handle_rfid_detection(self, mqtt):
        from sensors.rfid import RFIDSensor
        from outputs.rgb import RGB
        from outputs.buzzer import Buzzer
        from outputs.servo import Servo
        from display.oled import OLED
        from comms.supabase import Supabase

        rfid = RFIDSensor()
        rgb = RGB()
        buzzer = Buzzer()
        supabase = Supabase()
        door_servo = Servo(pin=13)
        oled = OLED()

        if rfid.scan_card():
            card_id = rfid.get_card_id()
            card_record = supabase.get_card_result(card_id)
            if card_record:
                rgb.set_color(0, 255, 0)
                door_servo.open()
                oled.show_text("ACCESS GRANTED", "Welcome home")
                payload = '{"card_id": "' + card_id + '", "access": "granted"}'
                if mqtt.publish("home/rfid", payload):
                    print("RFIDHandler - MQTT Publish OK")
                supabase.insert_rfid_scan(card_id, "granted", card_record['id'])
            else:
                rgb.set_color(255, 0, 0)
                buzzer.beep(3)
                oled.show_text("ACCESS DENIED", "Unauthorised access")
                payload = '{"card_id": "' + card_id + '", "access": "denied"}'
                if mqtt.publish("home/rfid", payload):
                    print("RFIDHandler - MQTT Publish OK")
                supabase.insert_rfid_scan(card_id, "denied", None)
        del rfid, rgb, buzzer, supabase, door_servo, oled
        self.memory.collect("After RFID handling")