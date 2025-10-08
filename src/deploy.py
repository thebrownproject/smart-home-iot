import os

def deploy():
    print("Deploying to ESP32...")
    try:
        # Use mpremote as a command-line tool
        result = os.system("mpremote connect /dev/tty.usbserial-10 cp -r src/ :")
        if result == 0:
            print("Deploy complete!")
        else:
            print("Deploy failed!")
    except Exception as e:
        print(f"Error deploying: {e}")

deploy()