from common.model.PlayerChooser.playerchooser import PlayerChooser
from common.model.player import Player
from simulator.gamestate import GameState


class TablePlayerChooser(PlayerChooser):

    def __init__(self):
        super().__init__('table-player chooser')

    def player(self, gamestate: GameState) -> Player:
        return gamestate.table_player()