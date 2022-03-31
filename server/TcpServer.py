from socket import *


class TcpServer:
    def __init__(self, host_name=None, server_port=None, sock=None):
        self.sock = None
        if sock:
            self.sock = sock
        else:
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.bind((host_name, server_port))
            self.sock.listen(5)
            print("I'm listening ...")
            temp, self.client_address = self.sock.accept()
            self.connection = TcpServer(sock=temp)
            print("connected to by address:`", self.client_address)

    def get_connection(self):
        return self.connection

    def receive(self):
        """
        :return: string ;the received data from the other end-system
        """
        message = self.connection.sock.recv(1024).decode()
        return message

    def send(self, message: str):
        """
        :param message: string ;the message to be sent to the other end-system
        """
        self.connection.sock.send(message.encode())

    def close(self):
        self.sock.close()


