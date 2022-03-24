from ui import *
from socket import *

hostName = '127.0.0.1'
serverPort = 2121

if __name__ == "__main__":
    ui = UI()
    while True:
        ui.get_command()
# controlSocket = socket(AF_INET, SOCK_STREAM)
# controlSocket.connect((hostName, serverPort))
# command = input("Enter a command: ")
# controlSocket.send(command.encode())
# response = controlSocket.recv(1024)
# print('server said: ', response.decode())
# controlSocket.close()

