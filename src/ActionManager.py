import threading
import time

from src.udp.config import *
from src.udp.SocketReceiver import SocketReceiver
from .TankController import TankController, ACTION_SHOOT, ACTION_ROTATE, ACTION_SHOOT_TARGET, controller_action_queue
from src.decision.decision import request_action


class ActionManager:
    """
    Singleton
    Polls action_queue and distributes tasks accordingly
    """
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
            self.mode = 0  # 0 = auto, 1 = manual

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
            if self.mode == 0:
                if self.tank_controller.busy is False:
                    action = request_action()
                    if action is not None:
                        controller_action_queue.update({action[0]: action[1]})
            else:
                if len(self.action_queue.keys()) != 0:
                    action = list(self.action_queue.items())[0]
                    if action[1] == ACTION_ROTATE:
                        controller_action_queue.update({action[0]: [action[1][0], action[1][1]]})
                    self.action_queue.pop(action[0])
            print("waiting for action")
            time.sleep(0.04)
