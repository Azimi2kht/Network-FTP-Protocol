from socket import *


class TcpServer:
    def __init__(self, host_name: str, server_port: int):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind((host_name, server_port))
        self.sock.listen(5)
        print("I'm listening ...")
        self.client_connection, self.client_address = self.sock.accept()
        print("connected to by address: ( ", self.client_address, " )")
    def get_clientconnection(self):
        
        return (self.client_connection)
 
    def receive(self):
        cl=self.get_clientconnection()
        
        message = (self.client_connection).recv(1024).decode()#
        print(message)
        return message    

    def send(self, message: str):
        self.sock.send(message.encode())

    # where to put the close function?!
