# main.py - Smart Home System Entry Point
from app import SmartHomeApp
from system_init import SystemInit

# Initialize system
system_init = SystemInit()

# Run startup sequence
system_init.init()

# Initialize app
app = SmartHomeApp(system_init)

# Run app
app.run()