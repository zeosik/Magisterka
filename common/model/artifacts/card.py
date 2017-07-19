from enum import Enum

from common.model.artifacts.artifact import Artifact

class CardColor(Enum):
    Clubs = 1 #trefl
    Diamonds = 2 #karo
    Hearts = 3 #serce
    Spades = 4 #pik

class UnknownCard(Artifact):
    def __init__(self):
        super().__init__('??')

class Card(Artifact):

    def __init__(self, rank: int, color: CardColor):
        super().__init__(str(rank) + color.name[0])
        self.rank = rank
        self.color = color
