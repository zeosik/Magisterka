from simulator import simulatorengine

class AnalysisAggregator:
    def __init__(self):
        self.analyzers = []

    def add_analyzer(self, analyzer):
        self.analyzers.append(analyzer)

    def print_final_result(self):
        print()
        print("Rezultat analizy:")
        print("Ilosc symulacji:", len(self.analyzers))

        weight_vector = dict()
        config_file = open("analyzer/parameter_values.txt", "r")
        for line in config_file.readlines():
            weight_vector[line.split()[0]] = float(line.split()[1])
        config_file.close()

        overal_score = 0
        for p_name, parameter in sorted(self.analyzers[0].parameters.items()):
            result = parameter.aggregate(self.analyzers)
            for item in result: # może być kilka wyników z jednego parametru (np średnia i wariancja)
                print("Wartosc dla parametru", item[0], ":", item[1])
                try:
                    overal_score += item[1] * weight_vector[item[0]]
                except (KeyError):
                    print("ERROR: W pliku parameter_values.txt nie ma wagi dla parametru", item[0])
                    return
        print("Wynik ogolny: ", overal_score)

def run(game_name, num_players, num_random_bots, num_simulations):
    analysis_aggregator = AnalysisAggregator()

    for n in range(num_simulations):
        print("Iteracja:", n + 1, "/", num_simulations)
        analyzer = simulatorengine.run(game_name, num_players, 0, num_random_bots, True)
        analysis_aggregator.add_analyzer(analyzer)

    analysis_aggregator.print_final_result()

    #Analizujemy gre dla konkretnej liczby graczy, czy sprawdzamy jak się zachowuje gdy graczy jest mniej i wiecej?