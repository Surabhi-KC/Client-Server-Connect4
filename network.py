import socket
import pickle
import ssl


class Network:
    def __init__(self):
        self.server="Server IP address" #change
        self.port=5555
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        self.context.load_verify_locations("Path to clients ssl certificate")
        self.context.check_hostname = False
        self.context.verify_mode = ssl.CERT_NONE
        self.client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client = self.context.wrap_socket(self.client, server_hostname=self.server)
        self.addr=(self.server,self.port)
        self.p=self.connect()

        
        
    def getP(self):
        return self.p
    
    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass
    
    def disconnect(self):
        self.client.close()
        
    def sending(self,data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)

        
