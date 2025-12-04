from machine import Pin
from mfrc522_i2c import mfrc522

class RFIDSensor:
    def __init__(self):
        self.rfid = mfrc522(22, 21, 0x28)
        self.rfid.PCD_Init()
        self.rfid.ShowReaderDetails()

    def scan_card(self):
        if self.rfid.PICC_IsNewCardPresent():
            if self.rfid.PICC_ReadCardSerial():
                return True
        return False

    def get_card_id(self):
        if self.rfid.uid.size > 0:
            uid = ""
            for byte in self.rfid.uid.uidByte[0:self.rfid.uid.size]:
                uid += str(byte)
            return uid
        return None
    
    def clear_card(self):
        """Reset the stored card UID to allow re-scanning"""
        self.rfid.uid.size = 0
        for i in range(10):
            self.rfid.uid.uidByte[i] = 0