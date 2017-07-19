import logging

from common.model.cardpicker.cardpicker import CardPicker
from common.model.rules.rule import Rule
from simulator.gamestate import GameState

class Move(Rule):

    def __init__(self, card_picker: CardPicker):
        super().__init__('Move: {0}'.format(card_picker.name))
        self.log = logging.getLogger(self.__class__.__name__)
        self.card_picker = card_picker
        self.register_input(self.card_picker)

    def apply(self, gamestate: GameState):
        cards = self.card_picker.submitted_choice()
        place_from = self.card_picker.source_place_picker.submitted()
        place_to = self.card_picker.target_place_picker.submitted()

        for card in cards:
            place_from.artifacts.remove(card)
            place_to.artifacts.append(card)
