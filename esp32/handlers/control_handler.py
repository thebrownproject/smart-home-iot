class ControlHandler:
    def __init__(self, rgb_manager, oled_manager, door_servo_manager, buzzer_manager):
        """Store references to shared managers."""
        self.rgb_manager = rgb_manager
        self.oled_manager = oled_manager
        self.door_servo_manager = door_servo_manager
        self.buzzer_manager = buzzer_manager

    def handle_rfid_response(self, topic, msg):
        import ujson

        try:
            data = ujson.loads(msg.decode())
            if data['access'] == 'granted':
                self.rgb_manager.show('rfid', (0, 255, 0), 3)
                self.oled_manager.show('rfid', "ACCESS", 3, "GRANTED")
                self.door_servo_manager.open(duration=5)
            elif data['access'] == 'denied':
                self.rgb_manager.show('rfid', (255, 0, 0), 3)
                self.oled_manager.show('rfid', "ACCESS", 3, "DENIED")
                self.buzzer_manager.start(duration=5)

        except Exception as e:
            print(f"Error handling RFID response: {e}")

    def handle_door_control(self, topic, msg):
        import ujson

        try:
            data = ujson.loads(msg.decode())
            if data['action'] == 'open':
                self.door_servo_manager.open(duration=5)
            elif data['action'] == 'close':
                self.door_servo_manager.close()
        except Exception as e:
            print(f"Error handling door control: {e}")

    def handle_window_control(self, topic, msg):
        import ujson
        from outputs.servo import Servo

        try:
            data = ujson.loads(msg.decode())
            window = Servo(pin=5)
            if data['action'] == 'open':
                window.open()
            elif data['action'] == 'close':
                window.close()
            del window
        except Exception as e:
            print(f"Error handling window control: {e}")

    def handle_fan_control(self, topic, msg):
        import ujson
        from outputs.fan import Fan

        try:
            data = ujson.loads(msg.decode())
            fan = Fan()
            if data['action'] == 'on':
                fan.on()
            elif data['action'] == 'off':
                fan.off()
            del fan
        except Exception as e:
            print(f"Error handling fan control: {e}")
        
        
