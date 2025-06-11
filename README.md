# Connect4 Game - Client-Server Implementation (2024)
A two player Connect4 game built with Python socket programming, featuring secure SSL certificate authentication. This project demonstrates client-server architecture where multiple clients can connect and play against each other through a central server.
Two players can connect and play Connect4 in real-time. All communication handled through a central server. Secure connections using OpenSSL certificates. Multi-threaded server handling multiple client connections. Clients and server can be run either on the same machine or on different machines. Server automatically groups clients into game pairs

##  Prerequisites
- python 3.x
- pygame
- socket
- pickle
- OpenSSL (for certificate generation)
- Network connectivity between client and server machines

## Steps to run the project:

### Generate SSL Certificates
```bash
# Generate private key
openssl genrsa -out private.key 2048

# Generate certificate
openssl req -new -x509 -key private.key -out certificate.crt -days 365  (for a year of validity)
```

### Configure Server
Edit `server.py` in server folder:
```python
# Update these paths and settings
(line no. 8) cert_path = "Path to server's ssl certificate"
(line no. 9) key_path = "Path to server's key file"
(line no. 11) server = "server's IP address"
```

### Configure Client
Edit `network.py` in client folder:
```python
# Update these settings
(line no.8) self.server="server's IP Address"
(line no.12) self.context.load_verify_locations("Path to client's ssl certificate")
```

### Run the Game
**Start the Server:**
```bash
cd server
python server.py
```

**Start Clients (run this twice for two players):**
```bash
cd client
python connect4.py
```

## References:
- [Python Game Menu Tutorial](https://www.youtube.com/watch?v=GMBqjxcKogA&list=WL&index=)
- [Python Socket Programming Tutorial](https://www.youtube.com/watch?v=Jr02fUyO5Qo)
