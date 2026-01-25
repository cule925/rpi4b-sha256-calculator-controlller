#!/usr/bin/env python3

import threading
import app_threads
from app_manager import AppManager
import sys

def parse_cmdline():

    # Default communication mode is I2C
    comm_mode = 0

    if "--comm-mode" in sys.argv:
        index = sys.argv.index("--comm-mode")
        try:
            comm_mode = int(sys.argv[index + 1])
        except (IndexError, ValueError):
            print("Usage: main.py --comm-mode <0|1>")
            sys.exit(1)

    return comm_mode

def main():

    comm_mode = parse_cmdline()

    print("Starting app ...")
    app_manager = AppManager(comm_mode)
    puzzle_generator_thread_id = threading.Thread(target = app_threads.puzzle_generator_thread, args = (app_manager,))

    print("Starting threads ...")
    puzzle_generator_thread_id.start()

    puzzle_generator_thread_id.join()
    print("Threads finished!")

if __name__ == "__main__":
    main()
