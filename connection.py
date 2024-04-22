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

    def __init__(self, server_addr ,pk, nb):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #Stores {addr, conn} in order to create a single connection
        self.clients = {}
        self.private_key = pk
        self.num_bits = nb
        self.sock.bind((server_addr, 6767))
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
        mutex.release()

        #Process Diffie-Hellman first
        public_key = DiffieHellman.calculate_public_key(self.private_key)
        print("Server pb: " + str(public_key))

        conn.sendall(str(public_key).encode())
        client_public_key = int(conn.recv(1024).decode())
        print("Server cpb: " + str(public_key))

        shared_key = DiffieHellman.calculate_shared_secret_key(self.private_key, client_public_key)

        print("Server sk: " + str(public_key))


        #Add the shared_key into the dictionary
        mutex.acquire()
        connections[addr] = (shared_key.to_bytes(64, 'big'), 'server')
        mutex.release()

        #Listen for each client connected

        #while(1):
            #conn.recv();


        


class client:

    def __init__(self, pk):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.private_key = pk

    def connect(self, addr):
        self.sock.connect((addr, 6767))
        public_key = DiffieHellman.calculate_public_key(self.private_key)
        print("Client pb: " + str(public_key))
        self.sock.sendall(str(public_key).encode())
        server_public_key = int(self.sock.recv(1024).decode())
        print("Client spb: " + str(server_public_key))
        shared_key = DiffieHellman.calculate_shared_secret_key(self.private_key, server_public_key)
        print("Client sk: " + str(shared_key))

        return shared_key
    
    #Listen for messages
    def receive_file(self):
        pass

class connection_handler:

    def __init__(self, server_addr = 'localhost'):
        self.private_key, self.num_bits = self.gen_private_key()
        self.gen_private_key()
        print("Private Key: " + str(self.private_key))
        self.client = client(self.private_key)
        self.server = server(server_addr ,self.private_key, self.num_bits)


    def connect(self, addr):
        if addr not in connections:
            mutex.acquire()
            shared_key = self.client.connect(addr)
            connections[addr] = (shared_key.to_bytes(64,'big'), 'client')
            mutex.release()          
    
    def gen_private_key(self):
        num_bits = random.randint(128, 512)
        num_bits = (num_bits // 8) * 8
        private_key_int = random.getrandbits(num_bits)
        return private_key_int, num_bits

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
    


if __name__ == '__main__':
    
    
    type_cmd = input("Type cmd = ")

    if(type_cmd == '1'):
        ch = connection_handler('127.0.0.6')
        ch.connect('localhost')
        print("Shared Key = :" + str(connections["localhost"][0]))
        exit()
    elif(type_cmd == '2'):
        ch = connection_handler('localhost')
        input("Enter to stop waiting")
        print("Shared Key = :" + str(next(iter(connections.values()))[0]))
        exit()
