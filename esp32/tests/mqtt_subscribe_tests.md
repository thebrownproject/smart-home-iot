Test 1: RFID Access Granted

- Topic: devices/esp32_main/rfid/response
- Payload: {"access": "granted", "card_id": "ABC123"}
- Triggers: ControlHandler.handle_rfid_response()
- Expected: Green RGB, door opens, OLED shows welcome

Test 2: RFID Access Denied

- Topic: devices/esp32_main/rfid/response
- Payload: {"access": "denied", "card_id": "XYZ999"}
- Triggers: ControlHandler.handle_rfid_response()
- Expected: Red RGB, buzzer sounds, OLED shows denied

Test 3: Door Control

- Topic: devices/esp32_main/control/door
- Payload: {"action": "open"} or {"action": "close"}
- Triggers: ControlHandler.handle_door_control()
- Expected: Door servo moves (no visual feedback)

Test 4: Window Control

- Topic: devices/esp32_main/control/window
- Payload: {"action": "open"} or {"action": "close"}
- Triggers: ControlHandler.handle_window_control()
- Expected: Window servo moves

Test 5: Fan Control

- Topic: devices/esp32_main/control/fan
- Payload: {"action": "on"} or {"action": "off"}
- Triggers: ControlHandler.handle_fan_control()
- Expected: Fan turns on/off
