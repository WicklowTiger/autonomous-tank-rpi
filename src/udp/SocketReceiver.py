import socket
import threading
import time

from src.udp.config import CLI_ID, JETSON_ID, CONNECTION_TIMEOUT_LIMIT
from src.shared.conversion import decode_message
from src.shared.indexing import get_action_index
from src.decision.decision import add_detection


class SocketReceiver:
    """
    Wrapper for socket
    Constructor takes IP:PORT + reference to message_queue
    Received messages are stored in message_queue
    """
    socket = None
    connections = {}

    def __init__(self, udp_ip: str, udp_port: int, message_queue):
        self.udp_ip = udp_ip
        self.udp_port = udp_port
        self.message_queue = message_queue
        self.socket_setup()
        self.connections_setup()

    def connections_setup(self):
        self.connections = {"CLI": 0}
        threading.Thread(target=self.run_timeout()).start()

    def socket_setup(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.udp_ip, self.udp_port))

    def cli_keep_alive(self):
        self.connections.update({"CLI": CONNECTION_TIMEOUT_LIMIT})

    def run(self):
        print(self.__class__.__name__ + ": starting listener!")
        while True:
            data, sender_address = self.socket.recvfrom(1024)
            if CLI_ID not in data and JETSON_ID not in data:
                continue
            elif CLI_ID in data:
                self.cli_keep_alive()
            print(f"Received message: {data} from {sender_address}")
            decoded = decode_message(data.decode("utf-8"))
            if decoded[0] is not None:
                if decoded[0] == "DETECTION":
                    add_detection(decoded[1])
                else:
                    self.message_queue.update({get_action_index(): decoded})

    def run_timeout(self):
        while True:
            for key, value in self.connections:
                if value == 0:
                    self.connections.pop(key)
                    print(f"Timing out {key} connection")
                    if key == "CLI":
                        self.message_queue = {}
                else:
                    self.connections.update({key: value - 1})
            time.sleep(0.5)
