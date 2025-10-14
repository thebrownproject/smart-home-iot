def insert_rfid_scan(card_id, result, authorised_card_id):
    import urequests
    from config import SUPABASE_URL, SUPABASE_ANON_KEY
    import ujson
    from utils.memory import Memory

    memory = Memory()

    try:
        url = SUPABASE_URL + "/rest/v1/rfid_scans"
        headers = {
            "apikey": SUPABASE_ANON_KEY,
            "Authorization": "Bearer " + SUPABASE_ANON_KEY,
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
        
        return success
    
    except Exception as e:
        print("Error inserting RFID scan:", e)
        return False
    
    finally:
        memory.collect("After RFID scan insertion")
        del urequests, ujson, memory