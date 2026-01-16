from app_device import AppDevice
import yaml

class AppConfig():

    def __init__(self, config_path):
        self.config_path = config_path
        self.load_config()

    def load_config(self):

        app_devices = {}

        # Load configuration as a dictionary
        with open(self.config_path) as f:
            raw_dict = yaml.safe_load(f)

        for name, properties in raw_dict.items():
            # Create a device instance, unpack properties
            app_devices[name] = AppDevice(name, **properties)

        # Convert into tuple
        self.devices = tuple(app_devices.values())
