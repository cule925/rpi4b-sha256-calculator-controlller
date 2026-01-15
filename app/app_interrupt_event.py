from evdev import InputDevice, ecodes, categorize
import select
from enum import StrEnum
from app_defines import WORKER_COUNT

# Set event devices for each worker
class EventDevice(StrEnum):
    EVDEV_1 = "/dev/input/event0"
    EVDEV_2 = "/dev/input/event1"

assert len(EventDevice) == WORKER_COUNT

class InterruptEvent():
    
    def __init__(self):

        # Get tuple of all event device enum values
        self.event_devices = tuple(e.value for e in EventDevice)

        # Create input device objects for each event device
        self.input_devices = [InputDevice(path) for path in self.event_devices]

        # Get file descriptors of the input devices
        self.device_fds = [dev.fd for dev in self.input_devices]

        # Create dictionary for mapping file descriptors to device indexes
        self.device_fd_to_index = {fd: idx for idx, fd in enumerate(self.device_fds)}

        print("Interrupt event initialized!")

    def wait_for_event(self):

        while True:
            # Wait for events and get read file descriptors only (ignore others)
            read_fds, _, _ = select.select(self.device_fds, [], [])

            # Iterate over read file descriptors
            for read_fd in read_fds:

                # Find the index and device for this read file descriptor
                device_index = self.device_fd_to_index[read_fd]
                input_device = self.input_devices[device_index]

                # Read all pending events on this device
                for event in input_device.read():
                    # Filter for button events
                    if event.type == ecodes.EV_KEY:
                        # Convert to high level key event
                        key_event = categorize(event)
                        # If key-pressed (interrupt)
                        if key_event.keystate == key_event.key_down:
                            return device_index
