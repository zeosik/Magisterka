from common.model.cardpicker.cardpicker import CardPicker
from common.model.places.place import Place
from simulator.gamestate import GameState

class PlayerInputPicker(CardPicker):

    def __init__(self, card_count):
        super().__init__('PlayerInputPicker', card_count)

    def cards(self, place: Place) -> []:
        #TODO
        pass