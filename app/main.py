#!/usr/bin/env python3

import threading
import app_threads
from app_manager import AppManager

def main():

    print("Starting app ...")
    app_manager = AppManager()
    puzzle_generator_thread_id = threading.Thread(target = app_threads.puzzle_generator_thread, args = (app_manager,))

    print("Starting threads ...")
    puzzle_generator_thread_id.start()

    puzzle_generator_thread_id.join()
    print("Threads finished!")

if __name__ == "__main__":
    main()
