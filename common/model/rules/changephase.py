from common.model.playerchooser.playerchooser import PlayerChooser
from common.model.phase import Phase
from common.model.rules.rule import Rule
from simulator.gamestate import GameState


class ChangePhase(Rule):
    def __init__(self, to_phase:Phase, player_chooser: PlayerChooser):
        super().__init__('Change phase to: {0} {1}'.format(to_phase.name, player_chooser.name))
        self.phase = to_phase
        self.player_chooser = player_chooser
        self.register_input(self.player_chooser)

    def apply(self, gamestate: GameState):
        player = self.player_chooser.submitted()
        if gamestate.current_player() != player:
            gamestate.switch_player(player, self.phase)
        else:
            gamestate.switch_phase(self.phase)
