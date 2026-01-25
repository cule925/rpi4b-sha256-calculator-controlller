# Raspberry Pi 4B SHA256 calculator controller

Clone this repository in your home directory on your Raspberry Pi 4B running Raspberry Pi OS.

## I2C master setup

Change your directory position to `firmware` and execute the `firmware_setup.sh` script with the argument `0`.

```
./firmware_setup.sh 0
```

The script will copy the `i2c_master/config.txt` file on the boot partition in `/boot/firmware/`. This will enable hardware I2C on GPIO 2 and GPIO 3 where the Raspberry Pi will be running as an I2C master at Baud rate of 400 kHz. Also, it will enable interrupt on GPIO 24 and GPIO 25 with which the I2C slaves will signal that data is ready. The device files for the interrupts will be `/dev/input/event0` and `/dev/input/event1`. The addresses of the I2C slaves need to be `0x08` and `0x09` and need to match the ordering of the GPIO interrupt pins (GPIO 24 for I2C device address 0x08 and GPIO 25 for I2C device address 0x09).

Also, the script will enable auto-loading the I2C device driver by writing `i2c-dev` in the `/etc/modules-load.d/i2c.conf` file and install `python3-evdev` and `python3-smbus2` Python packages system wide.

Power off your Raspberry Pi I2C master, connect the I2C slaves to it and power them up and then power up the Raspberry Pi. After the Raspberry Pi boots, change your directory position to `app` and start the application `main.py` by running:

```
python3 main.py --comm-mode 0
```

To dismantle everything first power off the Raspberry Pi I2C master and then power off the I2C slaves. After that disconnect the wires.

## SPI master setup

Change your directory position to `firmware` and execute the `firmware_setup.sh` script with the argument `1`.

```
./firmware_setup.sh 1
```

The script will copy the `spi_master/config.txt` file on the boot partition in `/boot/firmware/`. This will enable hardware SPI on GPIO 9 (MISO), GPIO 10 (MOSI), GPIO 11 (SCLK), GPIO 8 (CS0) and GPIO 7 (CS1) where the Raspberry Pi will be running as an SPI master. Also, it will enable interrupt on GPIO 24 and GPIO 25 with which the SPI slaves will signal that data is ready. The device files for the interrupts will be `/dev/input/event0` and `/dev/input/event1`. The chip select GPIOs of the SPI slaves need to be GPIO 8 and GPIO 7 and need to match the ordering of the GPIO interrupt pins (GPIO 24 for SPI device with CS GPIO 8 and GPIO 25 for SPI device with CS GPIO 7).

Also, the script will install `python3-spidev` Python packages system wide.

Power off your Raspberry Pi SPI master, connect the SPI slaves to it, power up the Raspberry Pi and then power them up. After the Raspberry Pi boots, change your directory position to `app` and start the application `main.py` by running:

```
python3 main.py --comm-mode 1
```

To dismantle everything first power off the SPI slaves and then power off the Raspberry Pi SPI master. After that disconnect the wires.
