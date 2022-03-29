
from FtpServer import *
from random import randint

server = FtpServer('127.0.0.1', 2121)

# request or (command) _sent_by_client or message
while(True):
  server.receive_from_control()

#random_port = randint(3000, 50000)

#client_control_connection.send(str(random_port).encode())

# sending data
#server.send_with_data("yo this is data", random_port)


