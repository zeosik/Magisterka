from enum import Enum

from common.model.artifacts.artifact import Artifact

class CardColor(Enum):
    Clubs = 1 #trefl
    Diamonds = 2 #karo
    Hearts = 3 #serce
    Spades = 4 #pik

class UnknownCard(Artifact):
    def __str__(self):
        return "??"

class Card(Artifact):

    def __init__(self, rank: int, color: CardColor):
        super().__init__()
        self.rank = rank
        self.color = color
    
    def __str__(self):
        color_char = None
        if (self.color == CardColor.Clubs):
            color_char = "C"
        elif (self.color == CardColor.Diamonds):
            color_char = "D"
        elif (self.color == CardColor.Hearts):
            color_char = "H"
        else:
            color_char = "S"
        return str(self.rank) + color_char