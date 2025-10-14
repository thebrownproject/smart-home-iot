def insert_motion_event():
    import urequests
    from config import SUPABASE_URL, SUPABASE_ANON_KEY
    import ujson
    from utils.memory import Memory

    memory = Memory()

    try:
        url = SUPABASE_URL + "/rest/v1/motion_events"
        headers = {
            "apikey": SUPABASE_ANON_KEY,
            "Authorization": "Bearer " + SUPABASE_ANON_KEY,
            "Content-Type": "application/json"
        }
        data = {
            "device_id": 1,
            "detected": True
        }
        response = urequests.post(url, headers=headers, data=ujson.dumps(data))
        success = (response.status_code == 201)
        response.close()
        return success
    
    except Exception as e:
        print("Error inserting motion event:", e)
        return False
    
    finally:
        memory.collect("After motion event insertion")
        del urequests, ujson, memory