from common.model.playerchooser.playerchooser import PlayerChooser
from common.model.player import Player
from common.model.playertype import PlayerType
from simulator.gamestate import GameState


class CurrentPlayerChooser(PlayerChooser):

    def __init__(self, for_type: PlayerType):
        super().__init__('current {0}'.format(for_type.name))
        self.type = for_type

    def auto_submitted_values(self, gamestate: GameState) -> list:
        return [gamestate.current_player_for_type(self.type)]
