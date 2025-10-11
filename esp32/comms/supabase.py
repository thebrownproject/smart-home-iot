import urequests
from config import SUPABASE_URL, SUPABASE_ANON_KEY
import ujson


class Supabase:
    def __init__(self):
        self.url = SUPABASE_URL
        self.anon_key = SUPABASE_ANON_KEY

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
            return success
        except Exception as e:
            print("Error inserting sensor log:", e)
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
            json_string = ujson.dumps(data)
            response = urequests.post(url, headers=headers, data=json_string.encode('utf-8'))
            success = (response.status_code == 201)
            response.close()
            return success
        except Exception as e:
            print("Error inserting RFID scan:", e)
            return False