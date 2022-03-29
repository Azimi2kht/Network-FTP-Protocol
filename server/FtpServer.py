from TcpServer import *
from random import randint
import os

class FtpServer:
    def __init__(self, host_name: str, server_port: int):
        self.host_name = host_name
        self.server_port = server_port
        self.control_connection = TcpServer(self.host_name, self.server_port)
        self.data_connection = None
        self.client_connection=(self.control_connection).get_clientconnection()
    
    def send_with_control(self, message: str):
        #random_port = randint(3000, 50000)
        self.control_connection.send(message)

    # what type is the data here?
    # where should the close function be? [2]
    def send_with_data(self, data, port: int):
        self.data_connection = TcpServer(self.host_name, port)
        client_connection, message = self.data_connection.receive()
        client_connection.send(data.encode())
  
    def receive_from_control(self):
        print("waiting for instruction")
        message = (self.client_connection).recv(1024).decode()
        print("received instruction: ",message)
        self.answer_commands(message)
       
        
    def answer_commands(self, msg:str):
        #if(msg=="quit"):
         # self.quit()
        if(msg=="list"):

          self.list_files()

        elif(msg=="pwd") :

          self.Show_Current_Directory()

        elif("cd"  in msg) :
          
          self.change_Current_Directory(msg[3:])

    def Show_Current_Directory(self):
        path = os.getcwd()
        (self.client_connection).send(path.encode())
           
    def change_Current_Directory(self,msg:str):
        print("cur dir set to:")
        os.chdir(msg)
        
        (self.client_connection).send(os.getcwd().encode())
        print(os.getcwd())
        print("new dir sent to client")

    def list_files(self):
          path = os.getcwd()
          dir_list = os.listdir(path)
          number_of_files=len(dir_list)
          
          (self.client_connection).send(str(number_of_files).encode())
          print("Files and directories in '", path, "' :")
    
        # print the list
          totalsize=0
          for item in dir_list:
            if(os.path.isdir(item)):
              

              pm=">   name: "+item+" size: "+str(os.path.getsize(item))+"b"
            else:  
              pm="name: "+item+" size: "+str(os.path.getsize(item))+"b"
            print(pm)
            self.client_connection.send(pm.encode())
            totalsize+=os.path.getsize(item)
        
          
          self.client_connection.send(str(totalsize).encode())
    '''''
    def get_dir_size(self,path):
               total = 0
               with os.scandir(path) as it:
                  for entry in it:
                    if entry.is_file():
                        total += entry.stat().st_size
                    elif entry.is_dir():
                       total += self.get_dir_size(entry.path)
                    return total'''