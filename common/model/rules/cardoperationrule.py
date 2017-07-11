from common.model.rules.rule import Rule
from common.model.player import Player
from common.model.places.place import Place

class CardOperationRule(Rule):

    def __init__(self, name):
        super().__init__(name)

    def find_place(self, player: Player, placename) -> Place:
        for place in player.places:
            if placename == place.name:
                return place