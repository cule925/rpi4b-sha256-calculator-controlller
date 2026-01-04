#!/usr/bin/env python3

import os
import hashlib
from smbus2 import SMBus, i2c_msg
from evdev import InputDevice, ecodes, categorize

# ----------------------------------------
I2C_BUS = 1

EVENT_DEVICE_1_I2C_ADDR = 0x08

EVENT_DEVICE_1 = "/dev/input/event0"

SHA256_MASK = 15
OFFSET_1 = 0x80000000
# ----------------------------------------

def generate_sha256():
    random_data = os.urandom(32)
    digest = hashlib.sha256(random_data).digest()
    return digest

def send_i2c_payload(bus, address, offset, mask, digest):
    payload = bytearray()
    payload.extend(offset.to_bytes(4, "big"))
    payload.extend(mask.to_bytes(1, "big"))
    payload.extend(digest)

    assert len(payload) == 37

    msg = i2c_msg.write(address, payload)
    bus.i2c_rdwr(msg)

    print("I2C: written 37 bytes")

def wait_for_event(dev):
    print(f"Waiting for button press on path: {dev.path}")

    for event in dev.read_loop():
        if event.type == ecodes.EV_KEY:
            key_event = categorize(event)

            if key_event.keystate == key_event.key_down:
                print("Event level low detected")
                return

def read_i2c_response(bus, address):
    msg = i2c_msg.read(address, 4)
    bus.i2c_rdwr(msg)

    data = bytes(msg)
    print(f"I2C: read 4 bytes")
    return data

def main():
    mask = SHA256_MASK
    digest = generate_sha256()
    print(f"Digest: {digest.hex()}")
    print(f"Mask: {mask}")

    dev_1 = InputDevice(EVENT_DEVICE_1)
    dev_1_i2c_addr = EVENT_DEVICE_1_I2C_ADDR
    offset_1 = OFFSET_1

    with SMBus(I2C_BUS) as bus:
        send_i2c_payload(bus, dev_1_i2c_addr, offset_1, mask, digest)
        wait_for_event(dev_1)
        value_bytes = read_i2c_response(bus, dev_1_i2c_addr)
        value = int.from_bytes(value_bytes, "little")
        value_digest = hashlib.sha256(value_bytes).digest()
        print(f"Value: {value}")
        print(f"Value digest: {value_digest.hex()}")

if __name__ == "__main__":
    main()
