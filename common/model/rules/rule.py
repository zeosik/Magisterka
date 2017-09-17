from typing import List, Dict

from common.model.playerinput import PlayerInput
from simulator.gamestate import GameState


class Rule:

    def __init__(self, name):
        self.name = name
        self.next = []
        self.inputs = []

    def apply(self, gamestate: GameState):
        pass

    def simple_name(self) -> str:
        return self.name

    def register_input(self, player_input: PlayerInput):
        self.inputs += (player_input.required_inputs())
        self.inputs.append(player_input)

    def player_inputs(self) -> List[PlayerInput]:
        return self.inputs

    def append_next(self, rule): #Rule
        self.next.append(rule)

    def rules_dict(self) -> Dict[str, list]:
        return { '': self.next }
