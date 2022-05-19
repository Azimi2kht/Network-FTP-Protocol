from FtpClient import *
from socket import *

FILE_UNAVAILABLE = '550 Requested action not taken. File unavailable'
FILE_CONFORMATION = '200 OK'

HOST_NAME = '127.0.0.1'
PORT_NUMBER = 2121

class Client:
    def __init__(self, host_name: str, server_port: int):
        self.host_name = host_name
        self.server_port = server_port
        self.connection = FtpClient(host_name, server_port)
        self.help()

    def get_command(self):
        command = input("\nEnter a command: ")
        if command.lower() == 'help':
            self.help()
        elif command.lower() == 'list':
            self.list_files()
        elif command.lower() == 'pwd':
            self.show_current_directory()
        elif command[:2].lower() == 'cd':
            self.change_directory(command)
        elif command[:4].lower() == 'dwld':
            self.download_file(command)

    def help(self):
        help_width = 20
        print(f'{"HELP":<{help_width}}: Show help')
        print(f'{"LIST":<{help_width}}: List files')
        print(f'{"PWD":<{help_width}}: Show current dir')
        print(f'{"CD dir_name":<{help_width}}: Change directory')
        print(f'{"DWLD file_path":<{help_width}}: Download file')
        print(f'{"QUIT":<{help_width}}: Exit\n')

    def list_files(self):
        # request for list
        print("\nrequesting files...\n")
        self.connection.send_with_control("list")
        response = self.connection.receive_from_control()
        print(response)
        print()

    def show_current_directory(self):
        print("\n`requesting path...\n")
        self.connection.send_with_control("pwd")
        path = self.connection.receive_from_control()
        print(path)

    def change_directory(self, command: str):
        print("\nchanging dir to: ", command[3:])
        print()
        self.connection.send_with_control(command)
        command = self.connection.receive_from_control()
        print("dir changed to: ", command)

    def download_file(self, command: str):
        file_name = command[5:]
        self.connection.send_with_control(command)

        data_port = self.connection.receive_from_control() # ok

        if data_port == 'file not found':
            print(data_port)
        else:
            data_socket = socket(AF_INET, SOCK_STREAM)
            data_socket.connect((self.host_name, int(data_port)))
            with open(file_name, 'wb') as file:
                data = b""
                while True:
                    section = data_socket.recv(1024)
                    data += section

                    if not section:
                        break

                file.write(data)
                file.close()
                data_socket.close()
                print("\ndownloaded successfully.\n")

                
myClient = Client(HOST_NAME, PORT_NUMBER)
while True:
    myClient.get_command()
