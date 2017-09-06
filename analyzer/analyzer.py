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

        for p_name, parameter in self.analyzers[0].parameters.items():
            result = parameter.aggregate(self.analyzers)
            for item in result: # może być kilka wyników z jednego parametru (np średnia i wariancja)
                print("Wartosc dla parametru", item[0], ":", item[1])

def run(game_name, num_players, num_simulations):
    analysis_aggregator = AnalysisAggregator()

    for n in range(num_simulations):
        print("Iteracja:", n + 1, "/", num_simulations)
        analyzer = simulatorengine.run(game_name, num_players, 0, True)
        analysis_aggregator.add_analyzer(analyzer)

    analysis_aggregator.print_final_result()

    #Analizujemy gre dla konkretnej liczby graczy, czy sprawdzamy jak się zachowuje gdy graczy jest mniej i wiecej?