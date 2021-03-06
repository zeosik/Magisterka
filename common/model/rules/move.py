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

    def simple_name(self):
        f = self.card_picker.source_place_picker.place.name
        t = self.card_picker.target_place_picker.place.name
        c = self.card_picker.simple_name()
        return 'Move {2} {0} -> {1}'.format(f, t, c)

    def apply(self, gamestate: GameState):
        cards = list(self.card_picker.submitted_choice())
        place_from = self.card_picker.source_place_picker.submitted()
        place_to = self.card_picker.target_place_picker.submitted()

        for card in cards:
            place_from.remove_artifact(card)
            place_to.add_artifact(card)
            if not card.was_moved_at_least_once:
                card.was_moved_at_least_once = True
