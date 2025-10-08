from src.sensors.dht11 import DHT11Sensor
from src.sensors.pir import PIRSensor
from src.actuators.buttons import Button1, Button2

dht11_sensor = DHT11Sensor()
pir_sensor = PIRSensor()
button1 = Button1()
button2 = Button2()
temperature_threshold = 25

class AutomationController:
    def __init__(self):
        self.dht11_sensor = DHT11Sensor()
        self.pir_sensor = PIRSensor()
        self.button1 = Button1()
        self.button2 = Button2()
    
    def monitor_temperature(self):
        self.dht11_sensor.read_data()
    
    def check_temperature_threshold(self):
        if self.dht11_sensor.get_temperature() > temperature_threshold:
            self.handle_temperature_threshold()


    def handle_motion_detection(self):
        pass

    def handle_security_alert(self):
        pass

    def setup_button_interrupts(self):
        pass