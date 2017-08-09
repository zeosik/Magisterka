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
        super().__init__(Card.display_name(rank, color))
        self.rank = rank
        self.color = color

    @staticmethod
    def display_name(rank, color) -> str:
        rank_map = {
            11: 'J',
            12: 'Q',
            13: 'K',
            14: 'A',
        }
        return rank_map.get(rank, str(rank)) + color.name[0]
