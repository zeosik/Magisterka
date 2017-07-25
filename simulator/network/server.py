import socket, select
import pickle
import dill as pickle
import logging

class Server():
    def __init__(self, num_players):
        self.log = logging.getLogger(self.__class__.__name__)
        self.num_players = num_players
        self.clients = dict()

        self.socket = socket.socket()
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.host = socket.gethostname()
        self.port = 12345
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
   
    def accept_clients(self):
        while len(self.clients) < self.num_players:
            c, addr = self.socket.accept()
            self.log.debug("Got connection from " + str(addr))
            c.send("OK".encode())
            data = c.recv(1024).decode()
            self.clients[data] = c
    
    def ask_for_choice(self, request, player_name):
        client = self.clients[player_name]
        client.send(pickle.dumps(request))
        answer = pickle.loads(client.recv(100000))
        return answer

    def close_connections(self):
        for clientname, client in self.clients.items():
            client.send(pickle.dumps("DIE"))
            client.close()
        self.socket.close()