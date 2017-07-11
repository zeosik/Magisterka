from common.model.player import Player
from simulator.gamestate import GameState


class PlayerChooser:

    def __init__(self, name):
        self.name = name

    def player(self, gamestate: GameState) -> Player:
        pass