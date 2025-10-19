from app import SmartHomeApp
from system_init import SystemInit

system_init = SystemInit()
system_init.init()

app = SmartHomeApp()
app.run()