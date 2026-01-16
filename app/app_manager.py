from app_hasher import Hasher
from app_worker_comm import WorkerCommI2C
from app_interrupt_event import InterruptEvent
from app_config import AppConfig
import sys

CONFIG_PATH="config.yaml"

class AppManager():

    def __init__(self, comm_mode):
        self.comm_mode = comm_mode
        self.threads_active = True

        self.config = AppConfig(CONFIG_PATH)
        self.hasher = Hasher(self.config.devices)

        if self.comm_mode == 0:
            print("Communication mode I2C.")
            self.worker_comm = WorkerCommI2C(self.config.devices)
        elif self.comm_mode == 1:
            print("Communication mode SPI not yet supported!")
            sys.exit(1)
        else:
            print("Invalid communication mode! Exiting ...")
            sys.exit(1)

        self.interrupt_event = InterruptEvent(self.config.devices)

        print("App manager initialized!")
