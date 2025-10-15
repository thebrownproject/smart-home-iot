class ControlHandler:
    def handle_rfid_response(self, topic, msg):
        import ujson
        from outputs.rgb import RGB
        from outputs.servo import Servo
        from display.oled import OLED
        from outputs.buzzer import Buzzer

        try:
            data = ujson.loads(msg.decode())
            rgb = RGB()
            oled = OLED()

            if data['access'] == 'granted':
                rgb.set_color(0, 255, 0)
                oled.show_text("ACCESS GRANTED", "Welcome home")
                door_servo = Servo(pin=13)
                door_servo.open()
                del door_servo

            elif data['access'] == 'denied':
                rgb.set_color(255, 0, 0)
                oled.show_text("ACCESS DENIED", "Access denied")
                buzzer = Buzzer()
                buzzer.start()
                del buzzer

            del rgb, oled
        except Exception as e:
            print(f"Error handling RFID response: {e}")

    def handle_door_control(self, topic, msg):
        import ujson
        from outputs.servo import Servo

        try:
            data = ujson.loads(msg.decode())
            door = Servo(pin=13)
            if data['action'] == 'open':
                door.open()
            elif data['action'] == 'close':
                door.close()
            del door
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
        
        
