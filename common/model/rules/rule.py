from simulator.gamestate import GameState


class Rule:

    def __init__(self, name):
        self.name = name

    def apply(self, gamestate: GameState):
        pass
