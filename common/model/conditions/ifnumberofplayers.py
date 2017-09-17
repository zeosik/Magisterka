from typing import Callable

from common.model.conditions.ifcondition import IfCondition
from common.model.playerchooser.constantplayerchooser import ConstantPlayerChooser
from common.model.playerchooser.playerchooser import PlayerChooser
from common.model.playertype import PlayerType
from simulator.gamestate import GameState


class IfNumberOfPlayers(IfCondition):

    def __init__(self, number_of_players: int, type: PlayerType, if_creator: Callable[[PlayerChooser], IfCondition]):
        super().__init__('number_of_players')
        self.number_of_players = number_of_players
        self.if_creator = if_creator
        self.type = type

    def evaluate(self, gamestate: GameState):
        number = 0
        for player in gamestate.players_for_type(self.type):
            condition = self.if_creator(ConstantPlayerChooser(player))
            if condition.evaluate(gamestate):
                number += 1
        return self.number_of_players == number
