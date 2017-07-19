from common.model.playerchooser.playerchooser import PlayerChooser
from common.model.player import Player
from simulator.gamestate import GameState


class TablePlayerChooser(PlayerChooser):

    def __init__(self):
        super().__init__('table-player chooser')

    def auto_submitted_values(self, gamestate: GameState) -> list:
        return [gamestate.table_player()]