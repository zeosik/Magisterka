from common.model.playerinput import PlayerInput
from simulator.gamestate import GameState


class RulePicker(PlayerInput):

    def __init__(self, all_rules):
        super().__init__('Rule picker')
        self.all_rules = all_rules

    def auto_submitted_values(self, gamestate: GameState):
        if len(self.all_rules) == 1:
            return self.all_rules
        return super().auto_submitted_values(gamestate)

    def all_choices(self, gamestate: GameState) -> list:
        return self.all_rules

    def submit_choices(self, choices: list):
        if len(choices) != 1:
            return False, 'Choose only one rule'
        return super().submit_choices(choices)
