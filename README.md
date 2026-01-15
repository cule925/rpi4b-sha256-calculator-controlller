# Raspberry Pi 4B SHA256 calculator controller

Clone this repository in your home directory on your Raspberry Pi 4B running Raspberry Pi OS.

## I2C master setup

Copy the `firmware/i2c_master/config.txt` file on the boot partition with the command:

```
sudo cp ~/rpi4b-i2c-master-sha256-calculator/firmware/i2c_master/config.txt /boot/firmware/config.txt
```

This will enable hardware I2C on GPIO 2 and GPIO 3 where the Raspberry Pi will be running as an I2C master at Baud rate of 400 kHz. Also, it will enable interrupt on GPIO 24 and GPIO 25 with which the I2C slaves will signal that data is ready. The device files for the interrupts will be `/dev/input/event0` and `/dev/input/event1`. The addresses of the I2C slaves need to be `0x08` and `0x09` and need to match the ordering of the GPIO interrupt pins (GPIO 24 for I2C device address 0x08 and GPIO 25 for I2C device address 0x09).

Also, enable auto-loading the I2C device driver using the following command:

```
echo "i2c-dev" | sudo tee /etc/modules-load.d/i2c.conf
```

Install the following Python packages system wide:

```
sudo apt install python3-evdev python3-smbus2
```

Power off your Raspberry Pi I2C master, connect the I2C slaves to it and power them up and then power up the Raspberry Pi. After the Raspberry Pi boots, start the app `main.py` by running:

```
python3 ~/rpi4b-i2c-master-sha256-calculator/app/main.py
```

To dismantle everything first power off the Raspberry Pi I2C master and then power off the I2C slaves. After that disconnect the wires.

## SPI master setup

**TODO:**
