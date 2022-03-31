from socket import *

BUFFER_SIZE = 1024


class TcpServer:
    def __init__(self, host_name, server_port):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind((host_name, server_port))
        self.sock.listen(5)
        print("I'm listening ...")
        self.connection, self.client_address = self.sock.accept()
        print("connected to by address:`", self.client_address)

    def get_connection(self):
        return self.connection

    def receive(self):
        """
        :return: string ;the received data from the other end-system
        """
        message = self.connection.recv(BUFFER_SIZE).decode()
        return message

    def send(self, message: str):
        """
        :param message: string ;the message to be sent to the other end-system
        """
        self.connection.send(message)

    def close_connection(self):
        self.sock.close()

    def close_sock(self):
        self.sock.close()
