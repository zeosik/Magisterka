from analyzer.parameters.parameter import Parameter
import numpy

class PlayerPhaseCounter(Parameter):
    def __init__(self):
        super().__init__("PlayerPhaseCounter")
        self.count = 0
        self.is_wanted_player_turn = False

    def run(self, gamestate):
        wanted_player = gamestate.type_players_dict[gamestate.model.player_types[0]][0]
        current_player = gamestate.current_player()

        # Licze nie liczbe ruchow, a liczbe tur, czyli pomiedzy musi byc inny gracz
        if current_player is wanted_player:
            if self.is_wanted_player_turn == False:
                self.is_wanted_player_turn = True
                self.count = self.count + 1
        else:
            self.is_wanted_player_turn = False

    def result(self):
        return self.count

    def aggregate(self, analyzers):
        values = []
        for a in analyzers:
            values.append(a.parameters[self.name].result())
        results = []
        results.append((self.name + " - srednia", numpy.average(values)))
        results.append((self.name + " - wariancja", numpy.var(values)))
        return results