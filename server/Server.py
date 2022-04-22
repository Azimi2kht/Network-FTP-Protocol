from FtpServer import *

server = FtpServer('127.0.0.1', 2121)

# request or (command) _sent_by_client or message
while True:
    request = server.receive_from_control()
    server.answer_requests(request)
