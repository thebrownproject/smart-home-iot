# main.py - Smart Home System Entry Point

from outputs.led import LED
from system_init import SystemInit

system_init = SystemInit()

system_init.init()

# TODO: Main application loop will go here
# For now, just keep system running
print("Main loop not implemented yet - entering Test Mode")