from common.model.places.place import Place
from simulator.gamestate import GameState

class CardPicker:

    def __init__(self, name, card_count):
        self.name = name
        self.card_count = card_count

    def cards(self, place: Place) -> []:
        pass