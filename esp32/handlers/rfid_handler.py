from utils.memory import Memory
from sensors.rfid import RFIDSensor
from outputs.buzzer import Buzzer

class RFIDHandler:
    def __init__(self):
        self.memory = Memory()
        self.rfid = RFIDSensor()  # Initialize once, reuse across calls

    def handle_rfid_detection(self, mqtt):
        from outputs.rgb import RGB
        from outputs.servo import Servo
        from display.oled import OLED
        from outputs.buzzer import Buzzer
        from config import TOPIC_RFID_REQUEST, TOPIC_RFID_RESPONSE
        import ujson
        from utils.time_sync import TimeSync


        rgb = RGB()
        door_servo = Servo(pin=13)
        oled = OLED()
        time_sync = TimeSync()
        card_id = self.rfid.get_card_id()
        buzzer = Buzzer()

        buzzer.stop()
        rgb.off()
        

        if card_id:
            rgb.set_color(0, 255, 0)
            door_servo.open()
            oled.show_text("ACCESS GRANTED", "Welcome home")
            payload = ujson.dumps({
                "card_id": card_id,
                "access": "granted",
                "timestamp": time_sync.get_iso_timestamp()
            })
            if mqtt.publish(TOPIC_RFID_RESPONSE, payload):
                print("RFIDHandler - MQTT Publish OK")
            self.rfid.clear_card()
        else:
            rgb.set_color(255, 0, 0)
            buzzer.start()
            payload = ujson.dumps({
                "card_id": card_id,
                "access": "denied",
                "timestamp": time_sync.get_iso_timestamp()
            })
            door_servo.close()
            if mqtt.publish(TOPIC_RFID_RESPONSE, payload):
                print("RFIDHandler - MQTT Publish OK")
        self.rfid.clear_card()
    del rgb, door_servo, oled, buzzer, time_sync
    self.memory.collect("After RFID handling")