#!/usr/bin/env python3

import os
import hashlib
from smbus2 import SMBus, i2c_msg
from evdev import InputDevice, ecodes, categorize
import select
import time

# ----------------------------------------
I2C_BUS = 1

EVENT_DEVICE_1_I2C_ADDR = 0x08
EVENT_DEVICE_2_I2C_ADDR = 0x09

EVENT_DEVICE_1 = "/dev/input/event0"
EVENT_DEVICE_2 = "/dev/input/event1"

SHA256_MASK = 15
OFFSET_1 = 0x00000000
OFFSET_2 = 0x00010000
# ----------------------------------------

def generate_sha256():
    random_data = os.urandom(32)
    digest = hashlib.sha256(random_data).digest()
    return digest

def send_i2c_payload(bus, address, offset, mask, digest):
    payload = bytearray()
    payload.extend(offset.to_bytes(4, "little"))
    payload.extend(mask.to_bytes(1, "little"))
    payload.extend(digest)

    assert len(payload) == 37

    payload_msg = i2c_msg.write(address, payload)
    bus.i2c_rdwr(payload_msg)

    print(f"I2C: written 37 bytes to {hex(address)}")

def wait_for_events(devices):

    print("Waiting for button events on devices:", [d.path for d in devices])

    # Get the file descriptors
    fds = [dev.fd for dev in devices]

    while True:
        rlist, _, _ = select.select(fds, [], [])
        for fd in rlist:
            dev = next(d for d in devices if d.fd == fd)
            for event in dev.read():
                if event.type == ecodes.EV_KEY:
                    key_event = categorize(event)
                    if key_event.keystate == key_event.key_down:
                        print("Event detected on {dev.path}")
                        return dev

def read_i2c_response(bus, address):
    msg = i2c_msg.read(address, 4)
    bus.i2c_rdwr(msg)

    data = bytes(msg)
    print(f"I2C: read 4 bytes from {hex(address)}")
    return data

def main():
    mask = SHA256_MASK
    digest = generate_sha256()
    print(f"Digest: {digest.hex()}")
    print(f"Mask: {mask}")

    dev_1 = InputDevice(EVENT_DEVICE_1)
    dev_2 = InputDevice(EVENT_DEVICE_2)

    devices = [dev_1, dev_2]
    i2c_addresses = [EVENT_DEVICE_1_I2C_ADDR, EVENT_DEVICE_2_I2C_ADDR]
    offsets = [OFFSET_1, OFFSET_2]

    with SMBus(I2C_BUS) as bus:

        for i, dev in enumerate(devices):
            send_i2c_payload(bus, i2c_addresses[i], offsets[i], mask, digest)
            time.sleep(0.001)

        triggered_dev = wait_for_events(devices)
        idx = devices.index(triggered_dev)
        i2c_addr = i2c_addresses[idx]
        value_bytes = read_i2c_response(bus, i2c_addr)
        value = int.from_bytes(value_bytes, "little")
        value_digest = hashlib.sha256(value_bytes).digest()
        print(f"Device {triggered_dev.path} value: {value}")
        print(f"Device {triggered_dev.path} value digest: {value_digest.hex()}")

if __name__ == "__main__":
    main()
