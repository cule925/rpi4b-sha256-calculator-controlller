from evdev import InputDevice, ecodes, categorize
import select

class InterruptEvent():

    def __init__(self, devices):
        self.devices = devices

        # Get tuple of all event devices from devices
        self.event_devices = tuple(device.event_device for device in self.devices)

        # Create input device objects for each event device
        self.input_devices = [InputDevice(path) for path in self.event_devices]

        # Get file descriptors of each input device
        self.input_device_fds = [input_dev.fd for input_dev in self.input_devices]

        # Create dictionary for mapping file descriptors to device indexes
        self.input_device_fd_to_index = {fd: idx for idx, fd in enumerate(self.input_device_fds)}

        print("Interrupt event initialized!")

    def wait_for_event(self):

        while True:
            # Wait for events and get read file descriptors only (ignore others)
            read_fds, _, _ = select.select(self.input_device_fds, [], [])

            # Iterate over read file descriptors
            for read_fd in read_fds:

                # Find the index and device for this read file descriptor
                device_index = self.input_device_fd_to_index[read_fd]
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
