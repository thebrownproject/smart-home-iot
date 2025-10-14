def insert_sensor_log(sensor_type, value, unit):
      """Insert sensor reading to sensor_logs table"""
      import urequests
      from config import SUPABASE_URL, SUPABASE_ANON_KEY
      import ujson
      from utils.memory import Memory

      memory = Memory()

      try:
          url = SUPABASE_URL + "/rest/v1/sensor_logs"
          headers = {
              "apikey": SUPABASE_ANON_KEY,
              "Authorization": "Bearer " + SUPABASE_ANON_KEY,
              "Content-Type": "application/json"
          }
          data = {
              "device_id": 1,
              "sensor_type": sensor_type,
              "value": value,
              "unit": unit
          }
          response = urequests.post(url, headers=headers, data=ujson.dumps(data))
          success = (response.status_code == 201)
          response.close()

          return success

      except Exception as e:
          print("Error inserting sensor log:", e)
          return False

      finally:
          # Cleanup imports
          memory.collect("After sensor log insertion")
          del urequests, ujson, memory