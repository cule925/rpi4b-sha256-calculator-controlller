# Raspberry Pi 4B SHA256 calculator

Clone this repository in your home directory on your Raspberry Pi running Raspberry Pi OS.

Copy the `config.txt` file on the boot partition with the command:

```
sudo cp ~/rpi4b-i2c-master/firmware/config.txt /boot/firmware/config.txt
```

This will enable hardware I2C on GPIO 2 and GPIO 3. Also, it will enable interrupt on GPIO 25. The device file for the interrupt is `/dev/input/event4`.

Also, enable auto-loading the I2C device driver using the following command:

```
echo "i2c-dev" | sudo tee /etc/modules-load.d/i2c.conf
```

Install the following Python packages system wide:

```
sudo apt install python3-evdev python3-smbus2
```
