class UI:
    help_width = 20

    def __init__(self):
        self.current_command = "help"
        self.help()
        self.get_command()

    def help(self):
        print(f'Welcome to the FTP client.\n')
        print(f'Call one of the following functions:\n')
        print(f'{"HELP":<{self.help_width}}: Show help')
        print(f'{"LIST":<{self.help_width}}: List files')
        print(f'{"PWD":<{self.help_width}}: Show current dir')
        print(f'{"CD dir_name":<{self.help_width}}: Change directory')
        print(f'{"DWLD file_path":<{self.help_width}}: Download file')
        print(f'{"QUIT":<{self.help_width}}: Exit\n')

    def get_command(self):
        self.current_command = input("Enter a command: ")
