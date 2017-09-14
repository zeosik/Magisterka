from analyzer.parameters.parameter import Parameter
from common.model.rules.move import Move
import numpy, itertools

class GameLenghtCounter(Parameter):
    def __init__(self):
        super().__init__("GameLenghtCounter")
        self.lenght = 0
        self.current_player = None
        
    def run(self, gamestate):
        if not gamestate.is_current_player_table_player():
            if not gamestate.current_player() == self.current_player:
                self.lenght += gamestate.model.time_per_move
                self.current_player = gamestate.current_player()

    def result(self):
        return self.lenght

    def aggregate(self, analyzers):
        values = []
        for a in analyzers:
            values.append(a.parameters[self.name].result())
        return [(self.name + "[s]", int(numpy.average(values)))]