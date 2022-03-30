from FtpClient import *


class Client:
    def __init__(self, host_name: str, server_port: int):
        self.host_name = host_name
        self.server_port = server_port
        self.connection = FtpClient(host_name, server_port)
        # self.connection.send_with_control("PWD")
        # self.port_message = self.connection.receive_from_control()
        # self.main_data = self.connection.receive_from_data(int(self.port_message))

    def get_command(self):
        command = input("Enter a command: ")
        if command.lower() == 'help':
            self.help()
            # elif self.command.lower() == 'quit':
        #  quit()
        elif command.lower() == 'list':
            self.list_files()
        elif command.lower() == 'pwd':
            self.show_current_directory()
        elif 'cd' in command.lower():
            self.change_current_directory(command.lower())

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

        number_of_files = self.connection.receive_from_control()
        print("number of files: ", number_of_files)
        i = 0
        for i in range(int(number_of_files)):
            pm = self.connection.receive_from_control()
            print(pm)

        totalsize = self.connection.receive_from_control()
        print("total directory size: ", totalsize, "b")

    def show_current_directory(self):
        print("requesting path...")
        self.connection.send_with_control("pwd")
        path = self.connection.receive_from_control()
        print(path)

    def change_current_directory(self, msg: str):
        print("changing dir to: ", msg[3:])
        self.connection.send_with_control(msg)
        path = self.connection.receive_from_control()
        print("dir changed to: ", path)


myClient = Client('127.0.0.1', 2121)
while True:
    myClient.get_command()
