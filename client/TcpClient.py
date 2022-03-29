from socket import *


class TcpClient:
    def __init__(self, host_name: str, server_port: int):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect((host_name, server_port))

    def send(self, message: str):
        self.sock.send(message.encode())

    def receive(self):
        response = self.sock.recv(1024).decode()#ino avaz kardi
        return response
    # where to put the close function?!
