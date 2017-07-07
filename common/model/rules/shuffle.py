from common.model.places.place import Place
from common.model.rules.rule import Rule


class Shuffle(Rule):
    def __init__(self, player_selector, place: Place):
        super().__init__('Shuffle {0}'.format(place.name))
        self.place = place
        #?
        self.player_selector = player_selector
