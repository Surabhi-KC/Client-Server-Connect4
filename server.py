import socket
from _thread import *
import pickle
from game import Game
import ssl


cert_path = r"C:\Users\Surabhi K C\connect4.com.crt"
key_path = r"C:\Users\Surabhi K C\connect4.com.key"

server = "192.168.43.247"
port = 5555

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(cert_path, key_path)
context.verify_mode = ssl.CERT_NONE
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((server, port))
except socket.error as e:
    str(e)
    
s.listen()
print("Waiting for a connection, server started")

ssock = context.wrap_socket(s, server_side=True)

games = {}
idCount = 0

 
def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))
    
    reply=""
    while True:
        try:
            data = conn.recv(4096).decode()
            if gameId in games:
                game = games[gameId]
                if not data:
                    break
                else:
                    if data == "get":
                        reply = game
                        conn.send(pickle.dumps(reply))
                        continue
                    elif data.split()[0] == "pos":
                        posp = data.split()[1]
                        game.pos_change(p ,int(posp))
                    elif data.split()[0] == "move":
                        move = data.split()[1]
                        row = data.split()[2]
                        game.play(p, int(move),int(row))  
                        game.update_board(p)  
                    elif data.split()[0] == "change":
                        game.change_turn()  
                    elif data.split()[0]=="win":
                        game.update_win(p)                  
                    reply = game
                    conn.sendall(pickle.dumps(reply))
            else:
                break
        except:
            break
    
    print("Lost connection")
    try:
        del games[gameId]
    except:
        pass
    idCount -= 1
    conn.close()
    

while True:
    conn, addr = ssock.accept()
    print("Connected to: ",addr)
    idCount+=1
    p=0
    gameId = (idCount-1)//2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        p = 1
        
    start_new_thread(threaded_client, (conn, p, gameId))