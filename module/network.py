import socket

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "172.25.164.130"#change this ip to ur current ip
        self.port = 5555
        self.addr = (self.host, self.port)
        self.id = self.connect()

    def connect(self):
        self.client.connect(self.addr)
        return self.client.recv(3048).decode()

    def send(self,data):
        try:
            self.client.send(str.encode(data))
            reply = self.client.recv(2048).decode()   
            return reply
        except socket.error as e: 
            return str(e)

