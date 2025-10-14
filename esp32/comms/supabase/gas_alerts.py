def insert_gas_alert():
    import urequests
    from config import SUPABASE_URL, SUPABASE_ANON_KEY
    import ujson
    from utils.memory import Memory

    memory = Memory()
    
    try:
        memory.collect("Before insert_gas_alert")
        url = SUPABASE_URL + "/rest/v1/gas_alerts"
        headers = {
            "apikey": SUPABASE_ANON_KEY,
            "Authorization": "Bearer " + SUPABASE_ANON_KEY,
            "Content-Type": "application/json"
        }
        data = {
            "device_id": 1,
            "sensor_value": 0
        }
        response = urequests.post(url, headers=headers, data=ujson.dumps(data))
        success = (response.status_code == 201)
        response.close()
        return success
    
    except Exception as e:
        print("Error inserting gas alert:", e)
        return False
    
    finally:
        memory.collect("After gas alert insertion")
        del urequests, ujson, memory