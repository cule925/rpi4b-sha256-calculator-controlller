from app_defines import WORKER_COMM_MODE
from app_hasher import Hasher
from app_worker_comm import WorkerCommI2C
from app_interrupt_event import InterruptEvent
import sys

class AppManager():
    
    def __init__(self):
        self.threads_active = True
        self.hasher = Hasher()

        if WORKER_COMM_MODE == 0:
            print("Communication mode I2C.")
            self.worker_comm = WorkerCommI2C()
        elif WORKER_COMM_MODE == 1:
            print("Communication mode SPI not yet supported!")
            sys.exit(1)
        else:
            print("Invalid communication mode! Exiting ...")
            sys.exit(1)

        self.interrupt_event = InterruptEvent()

        print("App manager initialized!")
