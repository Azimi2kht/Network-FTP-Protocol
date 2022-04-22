from FtpClient import *

FILE_UNAVAILABLE = '550 Requested action not taken. File unavailable'
FILE_CONFORMATION = '200 OK'


class Client:
    def __init__(self, host_name: str, server_port: int):
        self.host_name = host_name
        self.server_port = server_port
        self.connection = FtpClient(host_name, server_port)
        self.help()
        # self.connection.send_with_control("PWD")
        # self.port_message = self.connection.receive_from_control()
        # self.main_data = self.connection.receive_from_data(int(self.port_message))

    def get_command(self):
        command = input("Enter a command: ").lower()
        if command == 'help':
            self.help()
            # elif self.command == 'quit':
        #  quit()
        elif command == 'list':
            self.list_files()
        elif command == 'pwd':
            self.show_current_directory()
        elif command[:2] == 'cd':
            self.change_directory(command)
        elif command[:4] == 'dwld':
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
        print("requesting files...")
        self.connection.send_with_control("list")
        response = self.connection.receive_from_control()
        print(response)

    def show_current_directory(self):
        print("requesting path...")
        self.connection.send_with_control("pwd")
        path = self.connection.receive_from_control()
        print(path)

    def change_directory(self, command: str):
        # the following message doesn't make sense if the given path is invalid.
        print("changing dir to: ", command[3:])
        self.connection.send_with_control(command)
        command = self.connection.receive_from_control()
        print("dir changed to: ", command)

    def download_file(self, command: str):
        file_name = command[5:]
        self.connection.send_with_control(command)
        response = self.connection.receive_from_control()
        # check if the file exists.
        if response == FILE_UNAVAILABLE:
            print('The requested file does not exist in this directory.')
        else:
            print('Downloading the file...')
            # getting the data port:
            data_port = int(self.connection.receive_from_control())
            data = self.connection.receive_from_data(data_port)

            f = open(file_name, 'w')
            f.write(data)
            f.close()

            print('File downloaded.')


myClient = Client('127.0.0.1', 2121)
while True:
    myClient.get_command()
