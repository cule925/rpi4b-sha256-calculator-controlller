from smbus2 import SMBus, i2c_msg
from enum import IntEnum
from app_defines import WORKER_COUNT

I2C_BUS = 1
I2C_DATA_LEN_SEND = 38
I2C_DATA_LEN_RECV = 5

# Set I2C slave addresses for each worker
class I2CSlaveAddress(IntEnum):
    SLAVE_ADDR_1 = 0x08
    SLAVE_ADDR_2 = 0x09

assert len(I2CSlaveAddress) == WORKER_COUNT

class WorkerCommI2C():
    
    def __init__(self):
        self.bus = SMBus(I2C_BUS)

        # Get tuple of all I2C slave address enum values
        self.i2c_addresses = tuple(e.value for e in I2CSlaveAddress)

        print("Worker communication via I2C initialized!")

    def send_data(self, device_index, data):

        assert len(data) == I2C_DATA_LEN_SEND

        # Sends bytes to slave
        msg = i2c_msg.write(self.i2c_addresses[device_index], data)
        self.bus.i2c_rdwr(msg)
        print(f"I2C: Written {I2C_DATA_LEN_SEND} bytes to {hex(self.i2c_addresses[device_index])}.")

    def receive_data(self, device_index):

        msg = i2c_msg.read(self.i2c_addresses[device_index], I2C_DATA_LEN_RECV)
        self.bus.i2c_rdwr(msg)
        print(f"I2C: Read {I2C_DATA_LEN_RECV} bytes from {hex(self.i2c_addresses[device_index])}.")

        # Parse bytes
        data = bytes(msg)

        return data

class WorkerCommSPI():

    def __init__(self):
        pass

    def send_data(self, device_index, data):
        pass

    def receive_data(self, device_index):
        pass
