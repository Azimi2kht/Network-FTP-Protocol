from TcpClient import *


class FtpClient:
    def __init__(self, host_name: str, server_control_port: int):
        self.host_name = host_name
        self.server_control_port = server_control_port
        self.control_connection = TcpClient(self.host_name, self.server_control_port)
        self.data_connection = None

    def send_with_control(self, message: str):
        self.control_connection.send(message)

    def send_with_data(self, message: str):
        self.data_connection.send(message)

    # where should the close function be? [2]
    # this function may be unnecessary.
    # the port received from server should be given here.
    def receive_from_data(self, data_port: int):
        # creating connection.
        self.data_connection = TcpClient(self.host_name, data_port)
        # receive the main data.
        data = self.data_connection.receive()

        self.control_connection.close()

        return data

    def receive_from_control(self):
        message = self.control_connection.receive()
        return message
