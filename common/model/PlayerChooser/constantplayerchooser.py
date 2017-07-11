from common.model.PlayerChooser.playerchooser import PlayerChooser
from common.model.player import Player
from simulator.gamestate import GameState


class ConstantPlayerChooser(PlayerChooser):

    def __init__(self, player: Player):
        super().__init__('same player chooser')
        #nie moze sie nazywac tak samo jak funkcja :(
        self.to_player = player

    def player(self, gamestate: GameState) -> Player:
        return self.to_player