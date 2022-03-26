from socket import *
import commands

hostName = '127.0.0.1'
port = 2121

dataSocket = socket(AF_INET, SOCK_STREAM)
controlSocket = socket(AF_INET, SOCK_STREAM)

controlSocket.bind((hostName, port))

controlSocket.listen(5)
print("listening ...")

while True:
    # get the message
    connectionSock, address = controlSocket.accept()
    message = connectionSock.recv(1024).decode()

    # log
    print("from client: ", address, " message: ", message)

    # check if the message is valid
    response = commands.respond_to_message(message)
    
    # respond
    connectionSock.send(response.encode())
    connectionSock.close()

