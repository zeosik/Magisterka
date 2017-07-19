from typing import Callable

from common.model.playerchooser.constantplayerchooser import ConstantPlayerChooser
from common.model.playerchooser.playerchooser import PlayerChooser
from common.model.playertype import PlayerType
from common.model.rules.rule import Rule


class ForEachPlayer(Rule):
    def __init__(self, in_player_type: PlayerType, create_action_function: Callable[[PlayerChooser], Rule]):
        super().__init__('For each player in type {0} '.format(in_player_type.name))
        self.player_type = in_player_type
        self.create_action_func = create_action_function

        self.player_iterator = None
        self.current_player = None
        self.orginal_next = None

    def apply(self, gamestate):
        #czy zaczynamy iteracje
        if self.player_iterator is None:
            self.player_iterator = iter(gamestate.players_for_type(self.player_type))
            self.orginal_next = self.next

        try:
            self.current_player = next(self.player_iterator)
        except StopIteration:
            #przywracamy nastepna regule
            self.next = self.orginal_next

            self.player_iterator = None
            self.current_player = None
            self.orginal_next = None
        else:
            rule = self.create_action_func(ConstantPlayerChooser(self.current_player))
            rule.append_next(self)
            self.next = [rule]
