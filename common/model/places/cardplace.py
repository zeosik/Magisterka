from enum import Enum

from common.model.places.place import Place
from common.model.artifacts.card import UnknownCard

class CardVisibility(Enum):
    All = 1
    Player = 2
    Nobody = 3

class CardPlace(Place):
    def __init__(self, name, visibility : CardVisibility, starting_artifacts = []):
        super().__init__(name, starting_artifacts)
        self.visibility = visibility

    def get_cards(self, player = None):
        if player == None:
            return self.artifacts

        if len(self.artifacts) == 0:
            return []

        if self.visibility == CardVisibility.All:
            return self.get_cards_type_specific()

        if self.visibility == CardVisibility.Player:
            if player is self.player:
                return self.get_cards_type_specific()

        # wszystkie karty zakryte
        return [UnknownCard()] * len(self.artifacts)