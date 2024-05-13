import socket
import threading
import functions
from functions import P,G
import time
import random
import struct
from threading import Lock
from rc6 import encrypt_variable_length, decrypt_variable_length

mutex = Lock()
#Dictionary to store {addr, [common_key, type]} values
connections = {}
EOT = ' end_of_transmission '
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
        self.shutdown = False

    def start(self):
        self.sock.listen(5)
        while(True):
            conn, addr = self.sock.accept()
            print("Client addr = " + addr[0])
            if addr[0] in connections:
                continue
            client_threading = threading.Thread(target=self.process_client, args=(conn, addr[0]))
            client_threading.start()

    def process_client(self, conn, addr):
        try:
            mutex.acquire()
            self.clients[addr] = conn
            mutex.release()

            #Process Diffie-Hellman first
            public_key = DiffieHellman.calculate_public_key(self.private_key)

            conn.sendall(str(public_key).encode())
            client_public_key = int(conn.recv(1024).decode())

            shared_key = DiffieHellman.calculate_shared_secret_key(self.private_key, client_public_key)

            #Add the shared_key into the dictionary
            mutex.acquire()
            connections[addr] = (shared_key.to_bytes(64, 'big'), 'server')
            mutex.release()

            #Listen for each client connected
            nr0 = 0
            # See client version of receive_file to see more comments
            while not self.shutdown:
                data = b''
                full_msg = b''
                configuration_msg = b''
                data = conn.recv(16)
                print("Data = " + str(data))
                for byte_i in data:
                    try:
                        byte = bytes([byte_i])
                        byte.decode()
                        configuration_msg += byte
                    except UnicodeDecodeError:
                        full_msg += byte
                        
                configuration_msg = configuration_msg.decode()
                splitted = configuration_msg.split(" ")
                header = splitted[0]
                nr0 = int(splitted[1])
                msg_len = int(splitted[2])
                if header == "nr0":
                    eot_flag = False    
                    while len(full_msg) < msg_len:
                        new_data = conn.recv(msg_len)
                        full_msg += new_data
                        if self.shutdown:
                            break
                    eot_rcv = b''
                    if(len(full_msg) > msg_len):
                        for byte_i in full_msg[msg_len:]:
                            try:
                                byte = bytes([byte_i])
                                byte.decode()
                                eot_rcv += byte
                            except UnicodeDecodeError:
                                pass
                        if(eot_rcv.decode() == EOT):
                            eot_flag = True

                    while not eot_flag:
                        eot_data = conn.recv(1024)
                        eot_rcv += eot_data
                        eot_data = eot_rcv.decode()
                        if eot_data.find(EOT) != -1:
                            eot_flag = True
                        if self.shutdown:
                            break
                        
                    to_decrypt = full_msg[:msg_len]
                                
                    #Decrypt
                    decrypted = decrypt_variable_length(to_decrypt, connections[addr][0], nr0)
                    #Put into file
                    file_name = "./Received Data/" + addr + ".txt"
                    with open(file_name, 'w') as file:
                        file.write(decrypted.decode())
                    eot_flag = True

        except KeyboardInterrupt:
            print("Ended process")


        


class client:

    def __init__(self, pk):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.private_key = pk
        self.shutdown = False

    def connect(self, addr):
        self.sock.connect((addr, 6767))
        public_key = DiffieHellman.calculate_public_key(self.private_key)
        print("Client pb: " + str(public_key))
        self.sock.sendall(str(public_key).encode())
        server_public_key = int(self.sock.recv(1024).decode())
        print("Client spb: " + str(server_public_key))
        shared_key = DiffieHellman.calculate_shared_secret_key(self.private_key, server_public_key)
        print("Client sk: " + str(shared_key))

        #Launch receive_file thread
        recv_thread = threading.Thread(target=self.receive_file, args=(addr,))
        recv_thread.start()

        return shared_key
    
    #Listen for messages
    def receive_file(self, addr):
        try:     
            nr0 = 0
            while not self.shutdown:
                data = b''
                full_msg = b''
                configuration_msg = b''
                data = self.sock.recv(16)
                # Check if every byte from data can be decode, if not it means that it contains some bytes from the encryption message
                for byte_i in data:
                    try:
                        byte = bytes([byte_i])
                        byte.decode()
                        configuration_msg += byte
                    except UnicodeDecodeError:
                        full_msg += byte
                        
                configuration_msg = configuration_msg.decode()
                splitted = configuration_msg.split(" ")
                header = splitted[0]
                nr0 = int(splitted[1])
                msg_len = int(splitted[2])
                if header == "nr0":
                    eot_flag = False
                    # Receive while the len of the totally received bytes are less than than the total length specified in the configuration header
                    while len(full_msg) < msg_len:
                        print("Msg_curren_len = " + str(len(full_msg)))
                        new_data = self.sock.recv(msg_len)
                        full_msg += new_data
                        if self.shutdown:
                            break
                    eot_rcv = b''
                    # If the lenght of the received bytes are bigger than the total length it means that the message contains the end_of_transmission header it has to be removed
                    if(len(full_msg) > msg_len):
                        for byte_i in full_msg[msg_len:]:
                            try:
                                byte = bytes([byte_i])
                                byte.decode()
                                eot_rcv += byte
                            except UnicodeDecodeError:
                                pass
                        if(eot_rcv.decode() == EOT):
                            eot_flag = True

                    while not eot_flag:
                        eot_data = self.sock.recv(1024)
                        eot_rcv += eot_data
                        eot_data = eot_rcv.decode()
                        print("Eot data recv = " + eot_data)
                        if eot_data.find(EOT) != -1:
                            eot_flag = True
                        if self.shutdown:
                            break

                    # Decrypt the received text    
                    to_decrypt = full_msg[:msg_len]
                                
                    print("to_decrypt" + str(to_decrypt))
                    #Decrypt
                    decrypted = decrypt_variable_length(to_decrypt, connections[addr][0], nr0)
                    #Put into file with it's name as the ip address from whom it received
                    print("Decrypted = " + decrypted.decode())
                    file_name = "./Received Data/" + addr + ".txt"
                    with open(file_name, 'w') as file:
                        file.write(decrypted.decode())
                    eot_flag = True


        except KeyboardInterrupt:
            print("Ended process")




class connection_handler:

    def __init__(self, server_addr = 'localhost'):
        self.private_key, self.num_bits = self.gen_private_key()
        self.gen_private_key()
        print("Private Key: " + str(self.private_key))
        self.client = client(self.private_key)
        self.server = server(server_addr ,self.private_key, self.num_bits)
        self.private_key_bytes = self.private_key.to_bytes((self.private_key.bit_length() + 7)//8, 'big')


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
    
    def send_file(self, addr, file_name):
        #Open file and read it

        with open(file_name, 'r') as file:
            text = file.read()
            
        #Encrypt data
        encrypted, nr0 = encrypt_variable_length(text.encode(), connections[addr][0])
        en_splited = functions.split_in_pack_1376B(encrypted)

        header_nr0 = "nr0 " + str(nr0) + " " + str(len(encrypted))
        header_eot = EOT

        #While there is still encrypted data, send data
        #For each 1376 blocks of data sendall
        if(connections[addr][1] == 'client'):
            # Send configuration header
            self.client.sock.sendall(header_nr0.encode())
            time.sleep(0.1)
            # For each block of 1376 bytes send data
            for pack in en_splited:
                self.client.sock.sendall(pack)
            # Send EOT header to end current transaction
            self.client.sock.sendall(header_eot.encode())
            
        elif(connections[addr][1] == 'server'):
            # Send configuration header
            self.server.clients[addr].sendall(header_nr0.encode())
            time.sleep(0.1)
            for pack in en_splited:
                # For each block of 1376 bytes send data
                self.server.clients[addr].sendall(pack)
            # Send EOT header to end current transaction    
            self.server.clients[addr].sendall(header_eot.encode())        
        



class DiffieHellman:
    @staticmethod
    def calculate_public_key(private_key):
        return pow(G, private_key, P)
    
    @staticmethod
    def calculate_shared_secret_key(own_private_key, other_public_key):
        return pow(other_public_key, own_private_key, P)
    

# Used for testing

# if __name__ == '__main__':
    
    
#     type_cmd = input("Type cmd = ")

#     if(type_cmd == '1'):
#         ch = connection_handler('127.0.0.6')
#         ch.connect('localhost')
#         print("Shared Key = :" + str(connections["localhost"][0]))
#     elif(type_cmd == '2'):
#         ch = connection_handler('localhost')
#         input("Enter to stop waiting")
#         print("Shared Key = :" + str(next(iter(connections.values()))[0]))

#     while True:
#         try:
#             pass
#         except KeyboardInterrupt:
#             ch.client.sock.close()
#             ch.server.sock.close()

