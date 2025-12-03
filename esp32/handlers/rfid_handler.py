from utils.memory import Memory
from sensors.rfid import RFIDSensor

class RFIDHandler:
    def __init__(self):
        self.memory = Memory()
        self.rfid = RFIDSensor()
        self.card_id = 
        
    def handle_rfid_detection(self, mqtt, oled_manager):
        import ujson
        from utils.time_sync import TimeSync

        time_sync = TimeSync()

        if self.rfid.scan_card():
            card_id = self.rfid.get_card_id()
            print(f"[RFIDHandler] Card detected: {card_id}")
        else:
            del time_sync
            self.memory.collect("After RFID detection")
            return
        if card_id:
            self.publish(card_id, mqtt, oled_manager, time_sync)
        else:
            print(f"[RFIDHandler] Card scan succeeded but card_id is None/empty")
        del time_sync
        self.memory.collect("After RFID detection")

    def publish(self, card_id, mqtt, oled_manager):
        from config import TOPIC_RFID_REQUEST
        self.rfid.clear_card()

        payload = ujson.dumps({
            "card_id": card_id,
            "timestamp": time_sync.get_iso_timestamp()
        })
        print(f"[RFIDHandler] Publishing RFID request: {payload}")
        if mqtt.publish(TOPIC_RFID_REQUEST, payload):
            print(f"[RFIDHandler] RFID validation request sent to {TOPIC_RFID_REQUEST}")
        else:
            print("[RFIDHandler] MQTT publish failed - RFID request (card cleared to prevent re-scan)")
        oled_manager.show('rfid', "Card", 2, "detected")