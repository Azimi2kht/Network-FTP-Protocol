from socket import *

BUFFER_SIZE = 1024


class TcpClient:
    def __init__(self, host_name: str, server_port: int):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect((host_name, server_port))

    def send(self, message: str):
        self.sock.send(message.encode())

    def receive(self):
        response = self.sock.recv(BUFFER_SIZE).decode()
        return response

    def close(self):
        self.sock.close()
