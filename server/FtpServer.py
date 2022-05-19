from TcpServer import *
from random import randint
import os

FILE_UNAVAILABLE = '550 Requested action not taken. File unavailable'
FILE_CONFORMATION = '200 OK'
BUFFER_SIZE = 1024



def create_random_port():
    random_port = randint(3000, 50000)
    return random_port


class FtpServer:
    def __init__(self, host_name: str, server_port: int):
        self.host_name = host_name
        self.server_port = server_port
        self.connection = TcpServer(self.host_name, self.server_port)
        self.control_connection = self.connection.get_connection()
        self.data_connection = None

    def send_with_control(self, message: str):
        self.connection.send(message)

    # what type is the data here?
    # where should the close function be? [2]
    def send_with_data(self, data, port: int):
        self.data_connection = TcpServer(self.host_name, port)
        client_connection, message = self.data_connection.receive()
        client_connection.send(data.encode())

    def receive_from_control(self):

        print("waiting for instruction\n")
        message = self.connection.connection.recv(BUFFER_SIZE).decode()  # problem here.

        # client disconnecting.
        if message == "":
            print("client: ", self.connection.client_address, "has disconnected.\n")
            print("accepting connections ...")
            self.connection.connection, self.connection.client_address = self.connection.sock.accept()
            print("connected to by address:`", self.connection.client_address)
            message = self.connection.connection.recv(BUFFER_SIZE).decode()
            print("client said:", message)

        print("received instruction: ", message, "\n")
        return message

    def answer_requests(self, request: str):
        if request == "list":
            self.list_files()
        elif request == "pwd":
            self.show_current_directory()
        elif request[:2] == 'cd':
            self.change_current_directory(request[3:])
        elif request[:4] == 'dwld':
            self.download_file(request)

    def show_current_directory(self):
        path = os.getcwd()
        self.connection.connection.send(path.encode())

    def change_current_directory(self, path: str):
        print("cur dir set to:")
        os.chdir(path)

        self.connection.connection.send(os.getcwd().encode())
        print(os.getcwd())
        print("new dir sent to client")

    def list_files(self):
        path = os.getcwd()
        dir_list = os.listdir(path)
        number_of_files = len(dir_list)

        print("Files and directories in '", path, "' :")
       
        pm ="number of files: "+str(number_of_files)
        # print the list
        totalsize = 0
        for item in dir_list:
            if os.path.isdir(item):
                size=0
                for path, dirs, files in os.walk(item):
                    for f in files:
                      fp = os.path.join(item, f)
                      size += os.path.getsize(fp)
                pm += "\n"+">   name: " + item + " size: " + str(size) + "b"
                totalsize += size
            else:
                pm +="\n"+ "name: " + item + " size: " + str(os.path.getsize(item)) + "b"
                totalsize += os.path.getsize(item)
        
        pm+="\n"+"total directory size: "+str(totalsize)+"b"
        self.connection.connection.send(pm.encode())

    def download_file(self, request):
        file_name = request[5:]
        if file_name in os.listdir():
            data_port = create_random_port()
            data_socket = socket(AF_INET, SOCK_STREAM)
            data_socket.bind((self.host_name, data_port))
            data_socket.listen()
            self.connection.connection.send(str(data_port).encode())

            data_connection, cAddress = data_socket.accept()
            with open(file_name,'rb') as file:
                data_connection.send(file.read())
                file.close()
                data_connection.close()
        else:
            msg = 'file not found'
            self.connection.connection.send(msg.encode())
            
