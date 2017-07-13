from common.model.places.cardplace import CardPlace
from common.model.artifacts.card import UnknownCard

class CardLine(CardPlace):
    def __init__(self, name, starting_artifacts = []):
        super().__init__(name, starting_artifacts)
        
    def get_cards_type_specific(self, player = None):
        return self.artifacts


class FaceDownCardLine(CardLine):
    def is_visible_for_player(self, player):
        return False
    
class FaceUpCardLine(CardLine):
    def is_visible_for_player(self, player):
        return True

class PlayerCardLine(CardLine):
    def is_visible_for_player(self, player):
        if player is self.player:
            return True
        return False

class PlayerTypeCardLine(CardLine):
    def is_visible_for_player(self, player):
        if player.player_type is self.player.player_type:
            return True
        return False