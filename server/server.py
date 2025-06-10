import socket
from _thread import *
import pickle
from game import Game
import ssl


cert_path = "Path to server's ssl certificate"
key_path = "Path to server's key file"

server = "server's IP address"
port = 5555

#server socket creation
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(cert_path, key_path)
context.verify_mode = ssl.CERT_NONE #use only for self-signed certificates
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((server, port))
except socket.error as e:
    str(e)
    
s.listen()
print("Waiting for a connection, server started")

ssock = context.wrap_socket(s, server_side=True)

games = {}      #pairs of players
idCount = 0     #total number of players over all sets of games

 
def threaded_client(conn, p, gameId):
    """
        Thread for each client connected to server. Receiving and sending game/player information to other clients 
    Args:
        conn (ssl.SSLSocket): server socket
        p (int): player number
        gameId (int): game number
    """
    global idCount      
    conn.send(str.encode(str(p)))
    
    reply=""
    while True:
        try:
            data = conn.recv(4096).decode()
            if gameId in games:
                #only game info of current client's game is updated
                game = games[gameId]
                if not data:
                    break
                else:
                    #sending game info if request from other client is received
                    if data == "get":
                        reply = game
                        conn.send(pickle.dumps(reply))
                        continue
                    #updating player position above board based on data recived
                    elif data.split()[0] == "pos":
                        posp = data.split()[1]
                        game.pos_change(p ,int(posp))
                    #updating game pieces on board based on move made by player
                    elif data.split()[0] == "move":
                        move = data.split()[1]
                        row = data.split()[2]
                        game.play(p, int(move),int(row))  
                        game.update_board(p)  
                    #switching turns between players
                    elif data.split()[0] == "change":
                        game.change_turn()
                    #announcing winner of game  
                    elif data.split()[0]=="win":
                        game.update_win(p)   
                    #sending updated game info to all active clients               
                    reply = game
                    conn.sendall(pickle.dumps(reply))
            else:
                break
        except:
            break
    #deleting game object if either player exits or disconnects
    print("Lost connection")
    try:
        del games[gameId]
    except:
        pass
    idCount -= 1
    conn.close()
    
#loop to maintain list of active players and to group them into pairs
while True:
    conn, addr = ssock.accept()
    print("Connected to: ",addr)
    idCount+=1
    p=0
    gameId = (idCount-1)//2
    if idCount % 2 == 1:            #waiting for second player
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        p = 1
        
    start_new_thread(threaded_client, (conn, p, gameId))
