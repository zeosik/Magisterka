from random import randint
from common.model.places.place import Place
from common.model.rules.cardoperationrule import CardOperationRule
from common.model.player import SelectPlayer, PlayerChooser


class Shuffle(CardOperationRule):
    def __init__(self, player_selector: PlayerChooser, place: Place):
        super().__init__('Shuffle {0}'.format(place.name))
        self.place = place
        #?
        self.player_selector = player_selector
    
    def apply(self, gamestate):
        player = self.find_player(gamestate, self.player_selector)
        cards = self.find_place(player, self.place.name).artifacts

        for i in range(len(cards)):
            a = randint(0, len(cards) - 1)
            cards[i], cards[a] = cards[a], cards[i]