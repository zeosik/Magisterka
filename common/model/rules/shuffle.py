from random import randint

from common.model.PlayerChooser.playerchooser import PlayerChooser
from common.model.places.place import Place
from common.model.rules.rule import Rule


class Shuffle(Rule):
    def __init__(self, player_selector: PlayerChooser, place: Place):
        super().__init__('Shuffle {0}'.format(place.name))
        self.place = place
        #?
        self.player_selector = player_selector
    
    def apply(self, gamestate):
        player = self.player_selector.player(gamestate)
        cards = gamestate.actual_place(player, self.place).artifacts

        for i in range(len(cards)):
            a = randint(0, len(cards) - 1)
            cards[i], cards[a] = cards[a], cards[i]