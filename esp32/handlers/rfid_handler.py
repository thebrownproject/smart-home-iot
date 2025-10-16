from utils.memory import Memory
from sensors.rfid import RFIDSensor

class RFIDHandler:
    def __init__(self):
        self.memory = Memory()
        self.rfid = RFIDSensor()  # Initialize once, reuse across calls

    def handle_rfid_detection(self, mqtt, oled_manager):
        from config import TOPIC_RFID_REQUEST
        import ujson
        from utils.time_sync import TimeSync

        time_sync = TimeSync()

        # First scan for a card, then get its ID if found
        if self.rfid.scan_card():
            card_id = self.rfid.get_card_id()
            print(f"RFIDHandler - Card detected: {card_id}")
        else:
            # No card present, skip processing
            del time_sync
            self.memory.collect("After RFID detection")
            return

        if card_id:
            payload = ujson.dumps({
                "card_id": card_id,
                "timestamp": time_sync.get_iso_timestamp()
            })
            if mqtt.publish(TOPIC_RFID_REQUEST, payload):
                print("RFIDHandler - RFID validation request sent")
            else:
                print("RFIDHandler - Error sending RFID request")
            oled_manager.show('rfid', "Card", 2, "detected")
            self.rfid.clear_card()

        del time_sync
        self.memory.collect("After RFID detection")