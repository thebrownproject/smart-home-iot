from src.ui.display_manager import DisplayManager
from src.sensors.dht11 import DHT11Sensor
from src.sensors.pir import PIRSensor

class SmartHomeApp:
    def __init__(self):
        self.display_manager = DisplayManager()
        self.dht11_sensor = DHT11Sensor()
        self.pir_sensor = PIRSensor()
    def run(self):
        # self.dht11_sensor.read_data()
        # self.display_manager.display_data(self.dht11_sensor.get_temperature(), self.dht11_sensor.get_humidity())
        # print(self.dht11_sensor.get_temperature())
        self.display_manager.display_motion_data(self.pir_sensor.read_data())
# Test the SmartHomeApp class
app = SmartHomeApp()
app.run()