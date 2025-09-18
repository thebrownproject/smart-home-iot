from src.ui.display_manager import DisplayManager
from src.sensors.dht11 import DHT11Sensor

class SmartHomeApp:
    def __init__(self):
        self.display_manager = DisplayManager()
        self.dht11_sensor = DHT11Sensor()

    def run(self):
        self.dht11_sensor.read_data()
        self.display_manager.display_data(self.dht11_sensor.get_temperature(), self.dht11_sensor.get_humidity())
        print(self.dht11_sensor.get_temperature())

# Test the SmartHomeApp class
app = SmartHomeApp()
app.run()