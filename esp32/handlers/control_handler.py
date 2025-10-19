class ControlHandler:
    def __init__(self, rgb_manager, oled_manager, door_servo_manager, buzzer_manager):
        self.rgb_manager = rgb_manager
        self.oled_manager = oled_manager
        self.door_servo_manager = door_servo_manager
        self.buzzer_manager = buzzer_manager

    def handle_rfid_response(self, topic, msg):
        import ujson

        try:
            data = ujson.loads(msg.decode())
            if data.get('access') == 'granted':
                self.rgb_manager.show('rfid', (0, 255, 0), 3)
                self.oled_manager.show('rfid', "ACCESS", 3, "GRANTED")
                self.door_servo_manager.open(duration=5)
            elif data.get('access') == 'denied':
                self.rgb_manager.show('rfid', (255, 0, 0), 3)
                self.oled_manager.show('rfid', "ACCESS", 3, "DENIED")
                self.buzzer_manager.start(duration=5)
        except (ValueError, AttributeError) as e:
            print(f"Error parsing RFID response: {e}")

    def handle_door_control(self, topic, msg):
        import ujson

        try:
            data = ujson.loads(msg.decode())
            if data.get('action') == 'open':
                self.door_servo_manager.open(duration=5)
            elif data.get('action') == 'close':
                self.door_servo_manager.close()
        except (ValueError, AttributeError) as e:
            print(f"Error parsing door control: {e}")

    def handle_window_control(self, topic, msg):
        import ujson
        from outputs.servo import Servo

        try:
            data = ujson.loads(msg.decode())
            action = data.get('action')

            if action in ('open', 'close'):
                window = Servo(pin=5)
                if action == 'open':
                    window.open()
                elif action == 'close':
                    window.close()
                del window
        except (ValueError, AttributeError) as e:
            print(f"Error parsing window control: {e}")

    def handle_fan_control(self, topic, msg):
        import ujson
        from outputs.fan import Fan

        try:
            data = ujson.loads(msg.decode())
            action = data.get('action')
            if action in ('on', 'off'):
                fan = Fan()
                if action == 'on':
                    fan.on()
                elif action == 'off':
                    fan.off()
                del fan
        except (ValueError, AttributeError) as e:
            print(f"Error parsing fan control: {e}")
        
        
