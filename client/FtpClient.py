from TcpClient import *


class FtpClient:
    def __init__(self, host_name: str, server_control_port: int):
        self.host_name = host_name
        self.server_control_port = server_control_port
        self.control_connection = TcpClient(self.host_name, self.server_control_port)
        self.data_connection = None

    def send_with_control(self, message: str):
        self.control_connection.send(message)

    # where should the close function be? [2]
    # this function may be unnecessary.
    # the port received from server should be given here.
    def receive_from_data(self, port: int):
        # this snippet is to make a connection between client and server data_connection.
        message = "I am ready."
        self.data_connection = TcpClient(self.host_name, port)
        self.data_connection.send(message)

        # receive the main data
        data = self.data_connection.receive()
        print('From Data Channel: ', data)
        return data

    def receive_from_control(self):
        message = self.control_connection.receive()
        # print('From Control Channel: ', message)
        return message
