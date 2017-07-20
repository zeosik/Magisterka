from common.model.playerchooser.playerchooser import PlayerChooser
from common.model.playertype import PlayerType
from simulator.gamestate import GameState


class LastPlayerChooser(PlayerChooser):

    def __init__(self, player_type: PlayerType):
        super().__init__('Last Player Chooser')
        self.player_type = player_type

    def auto_submitted_values(self, gamestate: GameState):
        return [gamestate.players_for_type(self.player_type)[-1]]