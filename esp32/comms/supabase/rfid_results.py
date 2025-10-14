def get_card_result(card_id):
    import urequests
    from config import SUPABASE_URL, SUPABASE_ANON_KEY
    import ujson
    from utils.memory import Memory

    memory = Memory()

    try:    
        url = SUPABASE_URL + "/rest/v1/authorised_cards?card_id=eq." + card_id + "&is_active=eq.true"
        headers = {
            "apikey": SUPABASE_ANON_KEY,
            "Authorization": "Bearer " + SUPABASE_ANON_KEY,
            "Content-Type": "application/json"
        }
        response = urequests.get(url, headers=headers)
        cards = response.json()
        response.close()
        return cards[0] if cards else None
    
    except Exception as e:
        print("Error getting card result:", e)
        return False
    
    finally:
        memory.collect("After get_card_result")
        del urequests, ujson, memory