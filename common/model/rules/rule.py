from simulator.gamestate import GameState

class Rule:

    def __init__(self, name):
        self.name = name
        self.next = []

    def apply(self, gamestate: GameState):
        pass

    def player_inputs(self) -> list: #List[PlayerInput]
        return []

    def append_next(self, rule): #Rule
        self.next.append(rule)
