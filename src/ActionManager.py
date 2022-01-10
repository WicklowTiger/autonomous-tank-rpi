import threading
import time

from .config import *
from .SocketReceiver import SocketReceiver
from .TankController import TankController


class ActionManager:
    __instance = None

    def __init__(self):
        if ActionManager.__instance is not None:
            raise Exception(
                f"Can't instantiate singleton class more than once! Use {self.__class__.__name__}.get_instance()")
        else:
            ActionManager.__instance = self
            self.receiver_thread = None
            self.action_queue = {}
            self.tank_controller = TankController()

    @staticmethod
    def get_instance():
        if ActionManager.__instance is None:
            ActionManager()
        return ActionManager.__instance

    def run(self):
        socket_receiver = SocketReceiver(UDP_IP, UDP_PORT, self.action_queue)
        self.receiver_thread = threading.Thread(target=socket_receiver.run)
        self.receiver_thread.start()
        while True:
            if len(self.action_queue.keys()) != 0:
                action = list(self.action_queue.items())[0]
                self.action_queue.pop(action[0])
                self.tank_controller.set_angle(int(action[1]))
            print("waiting for action")
            time.sleep(2)
