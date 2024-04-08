import socket
import threading

SERVER = 1
CLIENT = 0


class connection:

    def __init__(self, con_type):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.con_type = con_type

    def start(self, host):
        if self.con_type == SERVER:
            self.sock.bind(socket.gethostbyname(),110568)
            self.sock.listen(5)
            server_thread = threading.Thread(target=self.sv_theading)
            server_thread.start()
        elif self.con_type == CLIENT:
            self.sock.connect((host, 110568)) 
    
    def sv_threading(self):
        while True:
            (clientsocket, address) = self.sock.accept() 
            ct = threading.Thread(target=self.client_thread,args=[clientsocket])
            ct.start()

    def client_thread(clientsocket):
        pass       