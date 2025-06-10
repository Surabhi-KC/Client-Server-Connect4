import socket
import pickle
import ssl


class Network:
    def __init__(self):
        self.server="server's IP Address"
        self.port=5555
        #checking ssl certificate
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        self.context.load_verify_locations("Path to client's ssl certificate")
        self.context.check_hostname = False             
        self.context.verify_mode = ssl.CERT_NONE        #Use only when dealing with self-signed certificates
        #client socket creation
        self.client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client = self.context.wrap_socket(self.client, server_hostname=self.server)
        self.addr=(self.server,self.port)
        self.p=self.connect()

    #get player number
    def getP(self):
        return self.p
    
    #connecting client to server
    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass
    
    def disconnect(self):
        self.client.close()
        
    #method to send game data to server
    def sending(self,data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)

        
