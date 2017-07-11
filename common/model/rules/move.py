import logging

from common.model.PlayerChooser.playerchooser import PlayerChooser
from common.model.places.place import Place
from common.model.playertype import PlayerType
from common.model.rules.cardoperationrule import CardOperationRule
from common.model.artifacts.card import Card

class Move(CardOperationRule):

    def __init__(self, from_player: PlayerChooser, from_place: Place, to_player: PlayerChooser, to_place:Place, number_of_cards, condition = None):
        super().__init__("Move from {0}:{1} to {2}:{3}".format(from_player.name, from_place.name, to_player.name, to_place.name))
        self.log = logging.getLogger(self.__class__.__name__)
        self.from_player = from_player
        self.from_place = from_place
        self.to_player = to_player
        self.to_place = to_place
        self.number_of_cards = number_of_cards
        self.condition = condition

    def apply(self, gamestate):

        if type(self.number_of_cards) is not int:
            #TODO obsługa wejścia?
            return

        real_player_from = self.from_player.player(gamestate)
        real_player_to = self.to_player.player(gamestate)

        real_place_from = self.find_place(real_player_from, self.from_place.name)
        real_place_to = self.find_place(real_player_to, self.to_place.name)

        #TODO condition
        #TODO karty przekładać z gory, z dołu, ze środka stosu?

        for i in range(self.number_of_cards):
            if len(self.from_place.artifacts) == 0:
                self.log.error("W " + self.from_place.artifacts.name + " nie ma kart")
                return
            real_place_to.artifacts.append(real_place_from.artifacts[-1])
            real_place_from.artifacts = real_place_from.artifacts[:-1]