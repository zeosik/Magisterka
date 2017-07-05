from common.model.artifacts.card import CardColor, Card


class CardGenerator():

    def __init__(self):
        pass

    @staticmethod
    def cards(min_rank:int , max_rank: int, colors: list):
        return [Card(rank, color) for rank in range(min_rank, max_rank + 1) for color in colors]