import logging

from common.model.PlayerChooser.playerchooser import PlayerChooser
from common.model.cardpicker.cardpicker import CardPicker
from common.model.cardpicker.topcardpicker import TopCardPicker
from common.model.cardpicker.playerinputpicker import PlayerInputPicker
from common.model.places.place import Place
from common.model.playertype import PlayerType
from common.model.rules.cardoperationrule import CardOperationRule
from common.model.artifacts.card import Card

class Move(CardOperationRule):

    def __init__(self, from_player: PlayerChooser, from_place: Place, to_player: PlayerChooser, to_place:Place, card_picker: CardPicker, condition = None):
        super().__init__("Move from {0}:{1} to {2}:{3}".format(from_player.name, from_place.name, to_player.name, to_place.name))
        self.log = logging.getLogger(self.__class__.__name__)
        self.from_player = from_player
        self.from_place = from_place
        self.to_player = to_player
        self.to_place = to_place
        self.card_picker = card_picker
        self.condition = condition

    def apply(self, gamestate):
        #TODO condition

        if type(self.card_picker) is PlayerInputPicker:
            #TODO obsługa wejścia?
            return

        real_player_from = self.from_player.player(gamestate)
        real_player_to = self.to_player.player(gamestate)

        real_place_from = self.find_place(real_player_from, self.from_place.name)
        real_place_to = self.find_place(real_player_to, self.to_place.name)

        cards = self.card_picker.cards(real_place_from)

        for card in cards:
            real_place_from.artifacts.remove(card)
        real_place_to.artifacts += cards