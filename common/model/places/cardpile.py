from common.model.places.cardplace import CardPlace
from common.model.artifacts.card import UnknownCard

class CardPile(CardPlace):
    def __init__(self, name, starting_artifacts = []):
        super().__init__(name, starting_artifacts)

    # to jesy stos, wiec widac tylko górna kartę
    def get_cards_type_specific(self, player = None):
        if len(self.artifacts) == 0:
            return []

        return [UnknownCard()] * (len(self.artifacts) -1) + [self.artifacts[-1]]


class FaceDownCardPile(CardPile):
    def is_visible_for_player(self, player):
        return False
    
class FaceUpCardPile(CardPile):
    def is_visible_for_player(self, player):
        return True

class PlayerCardPile(CardPile):
    def is_visible_for_player(self, player):
        if player is self.player:
            return True
        return False

class PlayerTypeCardPile(CardPile):
    def is_visible_for_player(self, player):
        if player.player_type is self.player.player_type:
            return True
        return False