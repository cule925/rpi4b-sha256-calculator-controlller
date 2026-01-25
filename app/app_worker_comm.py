from smbus2 import SMBus, i2c_msg
import spidev
import time

I2C_BUS = 1
I2C_DATA_LEN_SEND = 38
I2C_DATA_LEN_RECV = 5

# CPOL = 0, CPHA = 0
SPI_MODE = 0b00
SPI_MAX_SPEED_HZ = 1000000
SPI_TRANSACTION_SIZE = 40
SPI_MASTER_CMD_REQUEST_DATA_WRITE = 0x11
SPI_MASTER_CMD_WRITE_DATA = 0x22
SPI_MASTER_CMD_REQUEST_DATA_READ = 0x33
SPI_MASTER_CMD_DATA_READ = 0x44

class WorkerCommI2C():

    def __init__(self, devices):
        self.devices = devices
        self.bus = SMBus(I2C_BUS)

        # Get tuple of all I2C slave addresses from devices
        self.i2c_addresses = tuple(device.i2c_address for device in devices)

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

    def __init__(self, devices):
        self.devices = devices
        self.__open_spi_devices()

    def send_data(self, device_index, data):

        prepend_bytes = bytearray([SPI_MASTER_CMD_REQUEST_DATA_WRITE])
        append_bytes = bytearray([0x00] * (SPI_TRANSACTION_SIZE - 1))
        tx_data = prepend_bytes + append_bytes
        rx_data = self.spi_devices[device_index].xfer2(tx_data)
        print(f"SPI: CMD WRITE REQ - transaction of {SPI_TRANSACTION_SIZE} bytes to SPI device {device_index}.")

        time.sleep(0.02)

        prepend_bytes = bytearray([SPI_MASTER_CMD_WRITE_DATA])
        append_bytes = bytearray([0x00])
        tx_data = prepend_bytes + data + append_bytes
        assert len(tx_data) == SPI_TRANSACTION_SIZE

        rx_data = self.spi_devices[device_index].xfer2(tx_data)
        print(f"SPI: CMD WRITE - transaction of {SPI_TRANSACTION_SIZE} bytes to SPI device {device_index}.")

    def receive_data(self, device_index):

        prepend_bytes = bytearray([SPI_MASTER_CMD_REQUEST_DATA_READ])
        append_bytes = bytearray([0x00] * (SPI_TRANSACTION_SIZE - 1))
        tx_data = prepend_bytes + append_bytes
        rx_data = self.spi_devices[device_index].xfer2(tx_data)
        print(f"SPI: CMD READ REQ - transaction of {SPI_TRANSACTION_SIZE} bytes to SPI device {device_index}.")

        time.sleep(0.02)

        prepend_bytes = bytearray([SPI_MASTER_CMD_DATA_READ])
        append_bytes = bytearray([0x00] * (SPI_TRANSACTION_SIZE - 1))
        tx_data = prepend_bytes + append_bytes
        rx_data = self.spi_devices[device_index].xfer2(tx_data)
        print(f"SPI: CMD READ - transaction of {SPI_TRANSACTION_SIZE} bytes to SPI device {device_index}.")

        # Parse bytes
        data = bytes(rx_data[0:5])
        return data

    def __open_spi_devices(self):
        spi_open_devices = []
        for device in self.devices:
            bus_and_cs = device.spi_device[0]

            spi_open_device = spidev.SpiDev()
            spi_open_device.open(bus_and_cs["bus"], bus_and_cs["cs"])
            spi_open_device.mode = SPI_MODE
            spi_open_device.max_speed_hz = SPI_MAX_SPEED_HZ
            spi_open_devices.append(spi_open_device)

        self.spi_devices = tuple(spi_open_devices)
