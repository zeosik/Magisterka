from enum import Enum
import copy
from common.model.playertype import PlayerType

class Player:

    def __init__(self, name, player_type: PlayerType):
        self.name = name
        self.type = player_type
        self.isHuman = False
        self.places = copy.deepcopy(player_type.places)
        for place in self.places:
            place.set_player(self)
