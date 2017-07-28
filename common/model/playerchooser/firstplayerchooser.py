from common.model.playerchooser.playerchooser import PlayerChooser
from common.model.player import Player
from common.model.playertype import PlayerType
from simulator.gamestate import GameState


class FirstPlayerChooser(PlayerChooser):

    def __init__(self, for_type: PlayerType):
        super().__init__('first {0}'.format(for_type.name))
        self.type = for_type

    def auto_submitted_values(self, gamestate: GameState) -> list:
        return [gamestate.players_for_type(self.type)[0]]
