from simulator.gamestate import GameState


class IfCondition:

    def __init__(self, name):
        self.name = name

    def evaluate(self, gamestate: GameState) -> bool:
        pass
