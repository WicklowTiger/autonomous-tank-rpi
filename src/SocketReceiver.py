import socket

from src.shared.conversion import decode_message


class SocketReceiver:
    """
    Wrapper for socket
    Constructor takes IP:PORT + reference to message_queue
    Received messages are stored in message_queue
    """
    socket = None

    def __init__(self, udp_ip: str, udp_port: int, message_queue):
        self.udp_ip = udp_ip
        self.udp_port = udp_port
        self.message_queue = message_queue
        self.socket_setup()

    def socket_setup(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.udp_ip, self.udp_port))

    def run(self):
        print(self.__class__.__name__ + ": starting listener!")
        while True:
            data, sender_address = self.socket.recvfrom(1024)
            print(f"Received message: {data} from {sender_address}")
            decoded = decode_message(data.decode("utf-8"))
            self.message_queue.update({decoded[0]: decoded[1]})
