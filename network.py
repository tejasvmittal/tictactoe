import socket 
import pickle 


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.0.137"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()
    
    def getp(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()  # will return the player number returned by the server.
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048*2))  # returns the game object to the client
            # problem above ^
        except socket.error as e:
            print(e)
