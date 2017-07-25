import socket
import logging
import pickle

class Client():
    def __init__(self, name):
        self.log = logging.getLogger(self.__class__.__name__)
        self.name = name

        self.s = socket.socket()
        self.host = socket.gethostname()
        self.port = 12345

    def connect(self):
        self.s.connect((self.host, self.port))
        data = self.s.recv(1024)
        self.log.debug("Connected. Msg form server: " + data.decode())
        self.s.send(self.name.encode())

    def run(self):
        self.connect()

        while True:
            data = pickle.loads(self.s.recv(100000))
            if type(data) is str and data == "DIE":
                break
            
            gamestate = data[0]
            player = data[1]
            rule_picker = data[2]
            answer = self.player_turn(gamestate, player, rule_picker)
            self.s.send(pickle.dumps(answer))
        
        self.s.close