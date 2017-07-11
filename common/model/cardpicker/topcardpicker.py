from common.model.cardpicker.cardpicker import CardPicker
from common.model.places.place import Place
from simulator.gamestate import GameState

class TopCardPicker(CardPicker):

    def __init__(self, card_count):
        super().__init__('TopCardPicker', card_count)

    def cards(self, place: Place) -> []:
        #TODO przemyśleć czy kolejność ma tutaj znaczenie? (czy dobieramy na raz, czy po jednej?)
        return place.artifacts[-self.card_count:]