from common.model.PlayerInput import PlayerInput
from common.model.player import Player
from simulator.gamestate import GameState


class PlayerChooser(PlayerInput):

    def __init__(self, name):
        super().__init__(name)
        self.name = name

    #TODO przejsc na metode z playerinput ale to sam moge zrobic
    def player(self, gamestate: GameState) -> Player:
        pass

    def auto_submitted_values(self, gamestate: GameState) -> list:
        return [self.player(gamestate)]
