from random import randint

from common.model.placepicker.placepicker import PlacePicker
from common.model.rules.rule import Rule
from simulator.gamestate import GameState


class Shuffle(Rule):
    def __init__(self, place_picker: PlacePicker):
        super().__init__('Shuffle {0}'.format(place_picker.place.name))
        self.place_picker = place_picker
        self.register_input(self.place_picker)

    def apply(self, gamestate: GameState):
        place = self.place_picker.submitted()
        cards = place.artifacts()

        for i in range(len(cards)):
            a = randint(0, len(cards) - 1)
            cards[i], cards[a] = cards[a], cards[i]
