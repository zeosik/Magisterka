from analyzer.parameters.parameter import Parameter
from common.model.rules.move import Move
import numpy, itertools

class NumberOfMovesCounter(Parameter):
    def __init__(self):
        super().__init__("NumberOfMovesCounter")
        self.all_moves = []
        self.legal_moves = []
        
    def run(self, gamestate, rule_picker):
        single_all_moves = 0
        single_legal_moves = 0
        for rule in rule_picker.all_rules:
            if type(rule) is Move:  # tylko ruchy gdzie przekładamy karty
                for player_input in rule.player_inputs():
                # TODO tutaj chyba trochę to zadziała, licze prostą ilość możliwych wyborów, czyli jak będą
                # 2 miejsca i do kazdego będzie można przełożyć 1 z 3 kart to wyjdzie 2+3=5, a powinno być 2*3=6
                    if player_input.requires_player_input(gamestate):   # tylko tam gdzie mamy jakiś wybór
                        choices = player_input.all_choices(gamestate)
                        for length in range(len(choices) + 1):
                            for subset in itertools.combinations(choices, length):
                                single_all_moves += 1
                                if player_input.submit_choices(subset)[0]:
                                    single_legal_moves += 1
                        self.all_moves.append(single_all_moves)
                        self.legal_moves.append(single_legal_moves)

    def result(self):
        return (numpy.average(self.all_moves), numpy.average(self.legal_moves))

    def aggregate(self, analyzers):
        values_all, values_legal = [], []
        for a in analyzers:
            result = a.parameters[self.name].result()
            values_all.append(result[0])
            values_legal.append(result[1])
        results = []
        results.append((self.name + " - wszystkie, srednia", numpy.average(values_all)))
        results.append((self.name + " - legalne, srednia", numpy.average(values_legal)))
        return results