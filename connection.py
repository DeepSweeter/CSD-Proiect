import socket
import threading

class server:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(socket.gethostbyname(), 110568)
        self.start_thread = threading.Thread(target=self.start)
        self.start_thread.start()

    def start(self):
        self.sock.listen(5)
        while(True):
            conn, addr = self.sock.accept()
            client_threading = threading.Thread(target=self.process_client, args=(conn, addr))
            client_threading.start()

    def process_client(self, conn, addr):
        pass


class client:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        pass
