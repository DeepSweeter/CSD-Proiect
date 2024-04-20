import socket
import threading
import functions
from functions import P,G
import random
import struct
from threading import Lock

mutex = Lock()
#Dictionary to store {addr, [common_key, type]} values
connections = {}

class server:

    def __init__(self, pk, nb):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #Stores {addr, conn} in order to create a single connection
        self.clients = {}
        self.private_key = pk
        self.num_bits = nb
        self.sock.bind(functions.server_address, 110568)
        self.start_thread = threading.Thread(target=self.start)
        self.start_thread.start()

    def start(self):
        self.sock.listen(5)
        while(True):
            conn, addr = self.sock.accept()
            if addr in connections:
                continue
            client_threading = threading.Thread(target=self.process_client, args=(conn, addr))
            client_threading.start()

    def process_client(self, conn, addr):
        mutex.acquire()
        self.clients[addr] = conn
        connections[addr][1] = "server"
        mutex.release()

        #Process Diffie-Hellman first
        public_key = DiffieHellman.calculate_public_key(self.private_key)
        conn.sendall(str(public_key).encode())
        client_public_key = int(conn.recv(1024).decode())
        shared_key = DiffieHellman.calculate_shared_secret_key(client_public_key)

        #Add the shared_key into the dictionary
        mutex.acquire()
        connections[addr][0] = shared_key.to_bytes(self.num_bits // 8, 'big')
        mutex.release()

        #Listen for each client connected

        #while(1):
            #conn.recv();


        


class client:

    def __init__(self, pk):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.private_key = pk

    def connect(self, addr):
        self.sock.connect((addr, 110568))
        public_key = DiffieHellman.calculate_public_key(self.private_key)
        self.sock.sendall(str(public_key).encode())
        server_public_key = int(self.sock.recv(1024).decode())
        shared_key = DiffieHellman.calculate_shared_secret_key(server_public_key)
        return shared_key
    
    #Listen for messages
    def receive_file(self):
        pass

class connection_handler:

    def __init__(self):
        self.private_key= 0
        self.num_bits = 0
        self.gen_private_key()
        self.client = client(self.private_key)
        self.server = server(self.private_key, self.num_bits)


    def connect(self, addr):
        if addr not in connections:
            mutex.acquire()
            shared_key = self.client.connect(addr)
            connections[addr][1] = "client"
            connections[addr][0] = shared_key.to_bytes(self.num_bits,'big')
            mutex.release()          
    
    def gen_private_key(self):
        num_bits = random.randint(128, 512)
        self.num_bits = (num_bits // 8) * 8
        self.private_key_int = random.getrandbits(num_bits)
        #self.private_key = private_key_int.to_bytes(num_bits//8, 'big')
    
    def send_file(addr, file_name):
        #Open file and read it

        #Encrypt data

        #While there is still encrypted data, send data
            #For each 1376 blocks of data sendall
        
        #Finish transmission
        pass




            



class DiffieHellman:
    @staticmethod
    def calculate_public_key(private_key):
        return pow(G, private_key, P)
    
    @staticmethod
    def calculate_shared_secret_key(own_private_key, other_public_key):
        return pow(other_public_key, own_private_key, P)
    