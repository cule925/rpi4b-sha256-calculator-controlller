import os
import hashlib

SHA256_DIGEST_MASK = 15

class Hasher():

    def __init__(self, devices):
        self.devices = devices
        self.mask = SHA256_DIGEST_MASK

        # Get tuple of all input offsets from devices
        self.input_offsets = tuple(device.input_offset for device in self.devices)

        print("Hasher initialized!")

    def generate_digest(self):
        # Generate 32 random bytes and do a SHA256 digest on them
        random_input = os.urandom(32)
        digest = self.calculate_digest(random_input)
        return digest

    def get_input_offset(self, device_index):
        input_offset = self.input_offsets[device_index]
        return input_offset

    def calculate_digest(self, input):
        digest = hashlib.sha256(input).digest()
        return digest
