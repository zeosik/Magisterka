from common.model.conditions.ifcondition import IfCondition
from common.model.phase import Phase
from common.model.playerchooser.currentplayerchooser import CurrentPlayerChooser
from common.model.playertype import PlayerType
from simulator.gamestate import GameState


class IsCurrentPlayerInPhase(IfCondition):
    def __init__(self, phase: Phase, player_type: PlayerType):
        super().__init__('is phase')
        self.phase = phase
        self.player_type = player_type
        self.current_player_chooser = CurrentPlayerChooser(self.player_type)

    def evaluate(self, gamestate: GameState):
        # TODO to samo co w emptyplace, pozniej pomysle
        self.current_player_chooser.requires_player_input(gamestate)
        current = self.current_player_chooser.submitted()
        return gamestate.current_phase_for_player(current) is self.phase