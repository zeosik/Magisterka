from common.model.playerchooser.playerchooser import PlayerChooser
from common.model.rules.rule import Rule
from simulator.gamestate import GameState


class SkipPlayerTurn(Rule):

    def __init__(self, player_chooser: PlayerChooser):
        super().__init__('skip {0}'.format(player_chooser.name))
        self.player_chooser = player_chooser
        self.register_input(self.player_chooser)

    def apply(self, gamestate: GameState):
        player = self.player_chooser.submitted()
        gamestate.switch_player(player, gamestate.current_phase_for_player(player))
