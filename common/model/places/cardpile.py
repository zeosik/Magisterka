from common.model.places.cardplace import CardPlace, CardVisibility
from common.model.artifacts.card import UnknownCard

class CardPile(CardPlace):
    def __init__(self, name, visibility : CardVisibility, starting_artifacts = []):
        super().__init__(name, visibility, starting_artifacts)

    # to jesy stos, wiec widac tylko górna kartę
    def get_cards_type_specific(self, player = None):
        return [UnknownCard()] * (len(self.artifacts) -1) + [self.artifacts[-1]]