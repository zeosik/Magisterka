from common.model.artifacts.card import CardColor, Card


class CardGenerator():

    def __init__(self):
        pass

    @staticmethod
    def cards(min_rank:int , max_rank: int, colors: list):
        return [Card(rank, color) for rank in range(min_rank, max_rank + 1) for color in colors]

    @staticmethod
    def cards_standard_52():
        return CardGenerator.cards(2, 14, list(CardColor))

    @staticmethod
    def standard_cards_colors():
        return list(CardColor)
