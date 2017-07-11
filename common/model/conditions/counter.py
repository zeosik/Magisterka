from common.model.conditions.condition import Condition
from simulator.gamestate import GameState


class Counter(Condition):

    def __init__(self, evaluate_to_false_after):
        super().__init__('counter {0}'.format(evaluate_to_false_after))
        self.evaluate_to_false_after = evaluate_to_false_after

    def evaluate(self, gamestate: GameState) -> bool:
        self.evaluate_to_false_after = self.evaluate_to_false_after - 1
        return self.evaluate_to_false_after >= 0
