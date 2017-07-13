from enum import Enum

from common.model.places.place import Place
from common.model.artifacts.card import UnknownCard

class CardPlace(Place):
    def __init__(self, name, starting_artifacts = []):
        super().__init__(name, starting_artifacts)

    def get_cards(self, player = None):
        if player == None:
            return self.artifacts

        if self.is_visible_for_player(player):
            return self.get_cards_type_specific()
        else:
            return [UnknownCard()] * len(self.artifacts)
