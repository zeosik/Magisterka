from typing import Callable

from common.model.PlayerChooser.constantplayerchooser import ConstantPlayerChooser
from common.model.PlayerChooser.playerchooser import PlayerChooser
from common.model.playertype import PlayerType
from common.model.rules.rule import Rule


class ForEachPlayer(Rule):
    def __init__(self, in_player_type: PlayerType, create_action_function: Callable[[PlayerChooser], Rule]):
        super().__init__('For each player in type {0} '.format(in_player_type.name))
        self.player_type = in_player_type
        self.create_action_func = create_action_function

    def apply(self, gamestate):
        for player in gamestate.players_for_type(self.player_type):
            action = self.create_action_func(ConstantPlayerChooser(player))
            action.apply(gamestate)
