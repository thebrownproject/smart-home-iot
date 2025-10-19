from utils.memory import Memory

class ButtonHandler:
    def __init__(self):
        self.memory = Memory()
        self.gas_alarm_enabled = True
        self.pir_enabled = True
        self.gas_button_last_state = 1
        self.pir_button_last_state = 1
        self.gas_button_pressed = False
        self.pir_button_pressed = False

    def handle_buttons(self, oled_manager):
        from outputs.button import Button, BUTTON_GAS_ALARM_PIN, BUTTON_PIR_TOGGLE_PIN

        gas_button = Button(BUTTON_GAS_ALARM_PIN)
        pir_button = Button(BUTTON_PIR_TOGGLE_PIN)

        gas_current_state = 0 if gas_button.is_pressed() else 1
        if self.gas_button_last_state == 1 and gas_current_state == 0:
            self.gas_button_pressed = True
        self.gas_button_last_state = gas_current_state

        pir_current_state = 0 if pir_button.is_pressed() else 1
        if self.pir_button_last_state == 1 and pir_current_state == 0:
            self.pir_button_pressed = True
        self.pir_button_last_state = pir_current_state

        if self.gas_button_pressed:
            self.gas_alarm_enabled = not self.gas_alarm_enabled
            self.gas_button_pressed = False
            status = "Enabled" if self.gas_alarm_enabled else "Disabled"
            oled_manager.show('button', f"Gas Alarm", 3, status)
            print(f"[ButtonHandler] Gas alarm {status}")

        if self.pir_button_pressed:
            self.pir_enabled = not self.pir_enabled
            self.pir_button_pressed = False
            status = "Enabled" if self.pir_enabled else "Disabled"
            oled_manager.show('button', "Motion Sensor", 3, status)
            print(f"[ButtonHandler] Motion sensor {status}")

        del gas_button, pir_button
        self.memory.collect("After button handling")
