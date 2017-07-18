from common.model.rules.rule import Rule
from simulator.gamestate import GameState


class Pass(Rule):
    def __init__(self):
        super().__init__('PASS')

    def apply(self, gamestate: GameState):
        pass
