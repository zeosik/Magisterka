from common.model.PlayerChooser.playerchooser import PlayerChooser
from common.model.player import Player
from common.model.playertype import PlayerType
from simulator.gamestate import GameState


class CurrentPlayerChooser(PlayerChooser):

    def __init__(self, for_type: PlayerType):
        super().__init__('current player chooser')
        self.type = for_type

    def player(self, gamestate: GameState) -> Player:
        return gamestate.current_player_for_type(self.type)