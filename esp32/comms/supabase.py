import urequests
from config import SUPABASE_URL, SUPABASE_ANON_KEY
import ujson
import time
from utils.memory import Memory


class Supabase:
    def __init__(self):
        self.url = SUPABASE_URL
        self.anon_key = SUPABASE_ANON_KEY
        self.memory = Memory()

    def insert_sensor_log(self, sensor_type, value, unit):
        try:
            url = self.url + "/rest/v1/sensor_logs"
            headers = {
                "apikey": self.anon_key,
                "Authorization": "Bearer " + self.anon_key,
                "Content-Type": "application/json"
            }
            data = {
            "device_id": 1,
            "sensor_type": sensor_type,
            "value": value,
            "unit": unit
            }
            json_string = ujson.dumps(data)
            response = urequests.post(url, headers=headers, data=json_string.encode('utf-8'))
            success = (response.status_code == 201)
            response.close()
            self.memory.collect("After insert_sensor_log")
            return success
        except Exception as e:
            print("Error inserting sensor log:", e)
            return False
    
    def insert_motion_event(self):
        try:
            self.memory.collect("Before insert_motion_event")
            url = self.url + "/rest/v1/motion_events"
            headers = {
                "apikey": self.anon_key,
                "Authorization": "Bearer " + self.anon_key,
                "Content-Type": "application/json"
            }
            data = {
                "device_id": 1,
                "detected": True
            }
            response = urequests.post(url, headers=headers, data=ujson.dumps(data))
            success = (response.status_code == 201)
            response.close()
            self.memory.collect("After insert_motion_event")
            return success
        except Exception as e:
            print("Error inserting motion event:", e)
            return False
        
    def insert_rfid_scan(self, card_id, result, authorised_card_id=None):
        try:
            url = self.url + "/rest/v1/rfid_scans"
            headers = {
                "apikey": self.anon_key,
                "Authorization": "Bearer " + self.anon_key,
                "Content-Type": "application/json"
            }
            data = {
                "device_id": 1,
                "card_id": card_id,
                "access_result": result,
                "authorised_card_id": authorised_card_id
            }
            response = urequests.post(url, headers=headers, data=ujson.dumps(data))
            success = (response.status_code == 201)
            response.close()
            self.memory.collect("After insert_rfid_scan")
            return success
        except Exception as e:
            print("Error inserting RFID scan:", e)
            return False