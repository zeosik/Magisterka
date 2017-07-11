from common.model.conditions.condition import Condition
from common.model.rules.rule import Rule
from simulator.gamestate import GameState


class If(Rule):
    def __init__(self, condition: Condition, if_true: Rule, if_false: Rule):
        super().__init__('If condition {0} then {1} else {2}'.format(condition.name, if_true.name, if_false.name))
        self.if_true = if_true
        self.if_false = if_false
        self.condition = condition

    def apply(self, gamestate: GameState):
        if self.condition.evaluate(gamestate):
            self.if_true.apply(gamestate)
        else:
            self.if_false.apply(gamestate)
