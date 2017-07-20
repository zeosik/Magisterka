from common.model.conditions.ifcondition import IfCondition

#może jakas lepsza nazwa xd
from common.model.playerchooser.lastplayerchooser import LastPlayerChooser
from common.model.playertype import PlayerType
from simulator.gamestate import GameState


class NewRound(IfCondition):

    def __init__(self, player_type: PlayerType):
        super().__init__('New Round')
        self.player_type = player_type
        self.last_player_chooser = LastPlayerChooser(self.player_type)

    def evaluate(self, gamestate: GameState):
        #TODO to samo co w emptyplace, pozniej pomysle
        self.last_player_chooser.requires_player_input(gamestate)
        last_player = self.last_player_chooser.submitted()
        current_player = gamestate.current_player_for_type(self.player_type)
        return current_player is last_player
