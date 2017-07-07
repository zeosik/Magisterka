from common.model.places.place import Place
from common.model.playertype import PlayerType
from common.model.rules.rule import Rule


class Move(Rule):

    def __init__(self, from_player, from_place: Place, to_player, to_place:Place, number_of_cards, condition = None):
        super().__init__("Move from {0}:{1} to {2}:{3}".format(from_player.name, from_place.name, to_player.name, to_place.name))
        self.from_player = from_player
        self.from_place = from_place
        self.number_of_cards = number_of_cards
        self.condition = condition
