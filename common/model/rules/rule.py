from simulator.gamestate import GameState

class Rule:

    def __init__(self, name):
        self.name = name
        self.next = None

    def apply(self, gamestate: GameState):
        pass

    def player_inputs(self) -> list: #List[PlayerInput]
        return []
