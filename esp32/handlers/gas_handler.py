from utils.memory import Memory

class GasHandler:
    def __init__(self):
        self.memory = Memory()
        self.gas_alarm_active = False

    def handle_gas_detection(self, mqtt):
        from sensors.gas import GasSensor
        from outputs.rgb import RGB
        from outputs.fan import Fan
        from comms.supabase import Supabase
        from comms.mqtt_client import SmartHomeMQTTClient
        
        gas = GasSensor()
        rgb = RGB()
        fan = Fan()
        supabase = Supabase()
        mqtt = SmartHomeMQTTClient()

        
        if not self.gas_alarm_active:
            if gas.is_gas_detected():
                self.gas_alarm_active = True
                supabase.insert_gas_alert()
                self.memory.collect("GasHandler - Gas detected")
                rgb.set_color(255, 0, 0)
                fan.on()
                if mqtt.publish("home/gas", '{"detected": true}'):
                    print("GasHandler - MQTT Publish OK")
            else:
                print("GasHandler - No gas detected")
        else:
            if not gas.is_gas_detected():
                self.gas_alarm_active = False
                rgb.off()
                fan.off()
                if mqtt.publish("home/gas", '{"detected": false}'):
                    print("GasHandler - Gas cleared, MQTT Publish OK")
            else:
                print("GasHandler - Gas still detected, alarm active")
        
        del gas, rgb, fan, supabase
        self.memory.collect("After gas handling")