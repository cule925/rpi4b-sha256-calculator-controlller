#!/bin/bash

# Check if script ran as root
if [ "$EUID" -ne 0 ]; then
    echo "You must be root to run this."
    exit 1
fi

# Check for exactly one argument
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <0|1>"
    exit 1
fi

case "$1" in
    0)
        echo "Mode I2C master"
        cp i2c_master/config.txt /boot/firmware/config.txt
        echo "i2c-dev" | sudo tee /etc/modules-load.d/i2c.conf
        apt install python3-evdev python3-smbus2
        ;;
    1)
        echo "Mode SPI master"
        cp spi_master/config.txt /boot/firmware/config.txt
        apt install python3-spidev
        ;;
    *)
        echo "Usage: $0 <0|1>"
        exit 1
        ;;
esac
