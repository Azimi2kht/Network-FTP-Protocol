from ui import *
from socket import *

hostName = '127.0.0.1'
serverPort = 2121

# controlSocket = socket(AF_INET, SOCK_STREAM)
# controlSocket.connect((hostName, serverPort))

if __name__ == "__main__":
    while True:
        UI()
