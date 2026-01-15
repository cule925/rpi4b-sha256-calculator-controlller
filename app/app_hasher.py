import os
import hashlib
from enum import IntEnum
from app_defines import WORKER_COUNT

SHA256_DIGEST_MASK = 15

# Set input offsets for each worker
class InputOffset(IntEnum):
    INPUT_OFFSET_1 = 0x00000000
    INPUT_OFFSET_2 = 0x00010000

assert len(InputOffset) == WORKER_COUNT

class Hasher():

    def __init__(self):
        self.mask = SHA256_DIGEST_MASK

        # Get tuple of all input offset enum values
        self.input_offsets = tuple(e.value for e in InputOffset)

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
