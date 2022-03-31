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
        message = self.control_connection.recv(BUFFER_SIZE).decode()  # problem here.
        print("received instruction: ", message, "\n")
        return message

    def answer_requests(self, request: str):  # an "else" is needed here
        # if(msg=="quit"):
        # self.quit()
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
        self.control_connection.send(path.encode())

    def change_current_directory(self, path: str):
        print("cur dir set to:")
        os.chdir(path)

        self.control_connection.send(os.getcwd().encode())
        print(os.getcwd())
        print("new dir sent to client")

    def list_files(self):
        path = os.getcwd()
        dir_list = os.listdir(path)
        number_of_files = len(dir_list)

        self.control_connection.send(str(number_of_files).encode())
        print("Files and directories in '", path, "' :")

        # print the list
        totalsize = 0
        for item in dir_list:
            if os.path.isdir(item):
                pm = ">   name: " + item + " size: " + str(os.path.getsize(item)) + "b"
            else:
                pm = "name: " + item + " size: " + str(os.path.getsize(item)) + "b"
            print(pm)
            self.control_connection.send(pm.encode())
            totalsize += os.path.getsize(item)
        self.control_connection.send(str(totalsize).encode())

    def download_file(self, request):
        file_name = request[5:]
        # check if the file exists.
        if not os.path.isfile(file_name):
            self.control_connection.send(FILE_UNAVAILABLE.encode())
            print('there is no such file on the server:', file_name)
            return
        else:
            self.control_connection.send(FILE_CONFORMATION.encode())
            data_port = create_random_port()
            self.control_connection.send(str(data_port).encode())

            # creating the data socket:
            # listen
            self.data_connection = TcpServer(self.host_name, data_port)

            # prepare the file:
            f = open(file_name, 'r')
            file = f.read()
            f.close()
            # send
            self.data_connection.connection.send(file.encode())



    '''
    def get_dir_size(self,path):
               total = 0
               with os.scandir(path) as it:
                  for entry in it:
                    if entry.is_file():
                        total += entry.stat().st_size
                    elif entry.is_dir():
                       total += self.get_dir_size(entry.path)
                    return total    
    '''
