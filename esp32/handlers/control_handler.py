class ControlHandler:
    def __init__(self, rgb_manager, oled_manager, door_servo_manager, window_servo_manager, buzzer_manager, fan_manager):
        self.rgb_manager = rgb_manager
        self.oled_manager = oled_manager
        self.door_servo_manager = door_servo_manager
        self.window_servo_manager = window_servo_manager
        self.buzzer_manager = buzzer_manager
        self.fan_manager = fan_manager

    def handle_rfid_response(self, topic, msg):
        import ujson

        print(f"[ControlHandler] RFID response received on {topic}: {msg}")
        try:
            data = ujson.loads(msg.decode())
            print(f"[ControlHandler] Parsed RFID data: {data}")
            if data.get('access') == 'granted':
                print("[ControlHandler] ACCESS GRANTED - opening door")
                self.rgb_manager.show('rfid', (0, 255, 0), 3)
                self.oled_manager.show('rfid', "ACCESS", 3, "GRANTED")
                self.door_servo_manager.open(duration=5)
            elif data.get('access') == 'denied':
                print("[ControlHandler] ACCESS DENIED - activating buzzer")
                self.rgb_manager.show('rfid', (255, 0, 0), 3)
                self.oled_manager.show('rfid', "ACCESS", 3, "DENIED")
                self.buzzer_manager.start(duration=5)
            else:
                print(f"[ControlHandler] Unknown access value: {data.get('access')}")
        except (ValueError, AttributeError) as e:
            print(f"[ControlHandler] Error parsing RFID response: {e}")

    def handle_door_control(self, topic, msg, mqtt):
        import ujson
        from config import TOPIC_STATUS_DOOR
        from utils.time_sync import TimeSync

        try:
            data = ujson.loads(msg.decode())
            timestamp = TimeSync().get_iso_timestamp()

            if data.get('state') == 'open':
                self.door_servo_manager.open(duration=5)
                payload = ujson.dumps({
                    "state": "open",
                    "timestamp": timestamp
                })
                if not mqtt.publish(TOPIC_STATUS_DOOR, payload):
                    print("[ControlHandler] MQTT publish failed - door status (open)")
            elif data.get('state') == 'closed':
                self.door_servo_manager.close()
                payload = ujson.dumps({
                    "state": "closed",
                    "timestamp": timestamp
                })
                if not mqtt.publish(TOPIC_STATUS_DOOR, payload):
                    print("[ControlHandler] MQTT publish failed - door status (close)")
        except (ValueError, AttributeError) as e:
            print(f"Error parsing door control: {e}")

    def handle_window_control(self, topic, msg, mqtt):
        import ujson
        from config import TOPIC_STATUS_WINDOW
        from utils.time_sync import TimeSync

        try:
            data = ujson.loads(msg.decode())
            state = data.get('state')
            timestamp = TimeSync().get_iso_timestamp()

            if state in ('open', 'close'):
                if state == 'open':
                    self.window_servo_manager.open()
                    payload = ujson.dumps({
                        "state": "open",
                        "timestamp": timestamp
                    })
                    if not mqtt.publish(TOPIC_STATUS_WINDOW, payload):
                        print("[ControlHandler] MQTT publish failed - window status (open)")
                elif state == 'close':
                    self.window_servo_manager.close()
                    payload = ujson.dumps({
                        "state": "closed",
                        "timestamp": timestamp
                    })
                    if not mqtt.publish(TOPIC_STATUS_WINDOW, payload):
                        print("[ControlHandler] MQTT publish failed - window status (closed)")
        except (ValueError, AttributeError) as e:
            print(f"Error parsing window control: {e}")

    def handle_fan_control(self, topic, msg, mqtt):
        import ujson
        from config import TOPIC_STATUS_FAN
        from utils.time_sync import TimeSync

        try:
            data = ujson.loads(msg.decode())
            state = data.get('state')
            timestamp = TimeSync().get_iso_timestamp()

            if state in ('on', 'off'):
                if state == 'on':
                    self.fan_manager.on()
                    payload = ujson.dumps({
                        "state": "on",
                        "timestamp": timestamp
                    })
                    if not mqtt.publish(TOPIC_STATUS_FAN, payload):
                        print("[ControlHandler] MQTT publish failed - fan status (on)")
                elif state == 'off':
                    self.fan_manager.off()
                    payload = ujson.dumps({
                        "state": "off",
                        "timestamp": timestamp
                    })
                    if not mqtt.publish(TOPIC_STATUS_FAN, payload):
                        print("[ControlHandler] MQTT publish failed - fan status (off)")
        except (ValueError, AttributeError) as e:
            print(f"Error parsing fan control: {e}")
    
    def handle_status_request(self, topic, msg, mqtt, environment_handler):
        import ujson
        from utils.time_sync import TimeSync
        from config import TOPIC_RESPONSE_STATUS

        if self.fan_manager.is_on:
            fan_state = "on"
        else:
            fan_state = "off"

        if self.door_servo_manager.is_open:
            door_state = "open"
        else:
            door_state = "closed"

        if self.window_servo_manager.is_open:
            window_state = "open"
        else:
            window_state = "closed"

        payload = ujson.dumps({
            "fan": {
                "state": fan_state,
                "timestamp": TimeSync().get_iso_timestamp()
            },
            "door": {
                "state": door_state,
                "timestamp": TimeSync().get_iso_timestamp()
            },
            "window": {
                "state": window_state,
                "timestamp": TimeSync().get_iso_timestamp()
            },
            "temperature": environment_handler.last_temp,
            "humidity": environment_handler.last_humidity
        })
        if not mqtt.publish(TOPIC_RESPONSE_STATUS, payload):
            print("[ControlHandler] MQTT publish failed - status request")