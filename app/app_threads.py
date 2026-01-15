import time
from app_defines import WORKER_COUNT
from app_manager import AppManager

def puzzle_generator_thread(app_manager: AppManager):

    puzzle_id = 0
    mask = app_manager.hasher.mask

    while True == app_manager.threads_active:

        print(f"\n<========================= {puzzle_id} =========================>\n")

        # Generate new digest
        digest = app_manager.hasher.generate_digest()

        print(f"Digest: {digest.hex()}")
        print(f"Mask: {mask}")

        # Send the inputs of the puzzle
        for device_index in range(WORKER_COUNT):
            offset = app_manager.hasher.get_input_offset(device_index)

            # Create byte array
            input_data = bytearray()
            input_data.extend(offset.to_bytes(4, "little"))
            input_data.extend(mask.to_bytes(1, "little"))
            input_data.extend(digest)
            input_data.extend(puzzle_id.to_bytes(1, "little"))

            app_manager.worker_comm.send_data(device_index, input_data)
            time.sleep(0.001)

        # Check for solutions
        while True:

            # Wait for events and if there are any, read the data
            device_index = app_manager.interrupt_event.wait_for_event()
            receive_data = app_manager.worker_comm.receive_data(device_index)

            solution_offset = int.from_bytes(receive_data[:4], "little")
            solution_puzzle_id = receive_data[4]

            # If puzzle IDs match calculate the digest to verify
            if puzzle_id == solution_puzzle_id:
                solution_digest = app_manager.hasher.calculate_digest(solution_offset.to_bytes(4, "little"))
                device_path = app_manager.interrupt_event.input_devices[device_index].path
                print(f"Device '{device_path}' offset solution: {solution_offset}")
                print(f"Device '{device_path}' offset solution digest: {solution_digest.hex()}")

                # Increase the puzzle ID and generate the next puzzle to solve
                puzzle_id = (puzzle_id + 1) & 0xFF
                break
