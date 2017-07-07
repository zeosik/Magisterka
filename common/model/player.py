from enum import Enum
from common.model.playertype import PlayerType

class SelectPlayer(Enum):
    FirstPlayer = 1
    NextPlayer = 2
    CurrentPlayer = 3
    EachPlayer = 4
    TablePlayer = 5

class Player:

    def __init__(self, name, player_type: PlayerType):
        self.name = name
        self.type = player_type
