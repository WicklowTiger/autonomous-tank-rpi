import socket
import time


class SocketReceiver:
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
            self.message_queue.update({'rotate': data.decode("utf-8")})
