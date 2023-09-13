import socket 
import pickle 
from game import Game 
from _thread import * 

server = "192.168.0.137"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

games = {} # Key: game id, value: game object
playercount = 0 # increments each time a player joins the server.

def threaded_client(conn, player, gameid):
    """
    conn: the connection object in this case the client trying to connect to the server
    player: player number (0 or 1)
    data: if connection is successful data will contain instructions as follow:
        reset: to reset the game board
        get: to obtain the game object
        cell: the cell on which the player clicked on  
    """

    global playercount
    conn.send(str.encode(str(player)))

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()
            if gameid in games:
                game = games[gameid]
                if not data:
                    break
                else:
                    if data == "reset":
                        game.reset()
                    elif data != "get":
                        game.play(player, data)
                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameid]
        print("Closing Game", gameid)
    except:
        pass
    idCount -= 1
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    playercount += 1
    p = 0
    gameId = (playercount - 1)//2
    if playercount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        p = 1

    start_new_thread(threaded_client, (conn, p, gameId))
