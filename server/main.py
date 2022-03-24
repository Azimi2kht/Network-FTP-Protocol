from socket import *

hostName = '127.0.0.1'
port = 2121

dataSocket = socket(AF_INET, SOCK_STREAM)
controlSocket = socket(AF_INET, SOCK_STREAM)

controlSocket.bind((hostName, port))

controlSocket.listen(5)
print("listening ...")

while True:
    connectionSock, address = controlSocket.accept()
    msg = connectionSock.recv(1024).decode()
    print("from client: ", address, " message: ", msg)
    response = input('Response to the client :')
    connectionSock.send(response.encode())
    connectionSock.close()

