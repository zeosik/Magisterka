from common.model.conditions.ifcondition import IfCondition
from simulator.gamestate import GameState


class IfNot(IfCondition):

    def __init__(self, other_if: IfCondition):
        super().__init__('if not')
        self.other_if = other_if

    def evaluate(self, gamestate: GameState):
        return not self.other_if.evaluate(gamestate)
