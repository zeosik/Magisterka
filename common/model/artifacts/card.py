from enum import Enum

from common.model.artifacts.artifact import Artifact

class CardColor(Enum):
    Clubs = 1 #trefl
    Diamonds = 2 #karo
    Hearts = 3 #serce
    Spades = 4 #pik


class Card(Artifact):

    def __init__(self, rank: int, color: CardColor):
        super().__init__()
        self.rank = rank
        self.color = color