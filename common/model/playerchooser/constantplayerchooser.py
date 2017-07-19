from common.model.playerchooser.playerchooser import PlayerChooser
from common.model.player import Player
from simulator.gamestate import GameState


class ConstantPlayerChooser(PlayerChooser):

    def __init__(self, player: Player):
        super().__init__('same player chooser')
        self.player = player

    def auto_submitted_values(self, gamestate: GameState) -> list:
        return [self.player]