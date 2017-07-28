import logging

from common.model.conditions.ifcondition import IfCondition
from common.model.rules.rule import Rule
from simulator.gamestate import GameState


class If(Rule):
    def __init__(self, condition: IfCondition, if_true: Rule, if_false: Rule):
        super().__init__('If ({0})'.format(condition.name))
        self.log = logging.getLogger(self.__class__.__name__)
        self.if_true = []
        self.if_false = []
        self.condition = condition
        self.append_next_if_true(if_true)
        self.append_next_if_false(if_false)

    def apply(self, gamestate: GameState):
        if self.condition.evaluate(gamestate):
            self.next = self.if_true
        else:
            self.next = self.if_false

    def append_next(self, rule):
        self.log.error('cannot append next rule to IfRule, use append_next_if_true/false')
        raise Exception()

    def append_next_if_true(self, rule):
        self.if_true.append(rule)

    def append_next_if_false(self, rule):
        self.if_false.append(rule)