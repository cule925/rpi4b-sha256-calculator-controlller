class AppDevice():

    def __init__(self, name, event_device, input_offset, i2c_address):
        self.name = name
        self.event_device = event_device
        self.input_offset = input_offset
        self.i2c_address = i2c_address
