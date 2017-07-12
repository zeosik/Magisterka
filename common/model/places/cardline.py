from common.model.places.cardplace import CardPlace, CardVisibility
from common.model.artifacts.card import UnknownCard

class CardLine(CardPlace):
    def __init__(self, name, visibility : CardVisibility, starting_artifacts = []):
        super().__init__(name, visibility, starting_artifacts)
        
    def get_cards_type_specific(self, player = None):
        return self.artifacts