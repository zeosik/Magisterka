from simulator import simulatorengine

class AnalysisAggregator:
    def __init__(self):
        self.analyzers = []

    def add_analyzer(self, analyzer):
        self.analyzers.append(analyzer)

    def print_final_result(self):
        num_analyzers = len(self.analyzers)
        num_parameters = len(self.analyzers[0].parameters)

        results = dict()
        for i in range(num_parameters):
            name = self.analyzers[0].parameters[i].name
            values = []
            for a in self.analyzers:
                values.append(a.parameters[i].result())
            #liczę średnią wartość dla każdego parametru
            avg = sum(values)/len(values)
            results["'" + name + " - srednia'"] = avg
            
            values = []
            for a in self.analyzers:
                values.append((a.parameters[i].result() - avg)**2)
            #liczę wariancję dla każdego parametru (o ile czegoś nie pomyliłem...)
            variance = sum(values)/len(values)
            results["'" + name + " - wariancja'"] = variance

        print()
        print("Rezultat analizy:")
        print("Ilosc symulacji:", num_analyzers)
        for name, value in results.items():
            print("Wartosc dla parametru", name, ":", value)

def run(game_name, num_players, num_simulations):
    analysis_aggregator = AnalysisAggregator()

    for n in range(num_simulations):
        print()
        print("Iteracja:", n + 1, "/", num_simulations)
        print()
        analyzer = simulatorengine.run(game_name, num_players, 0, True)
        analysis_aggregator.add_analyzer(analyzer)

    analysis_aggregator.print_final_result()

    #Analizujemy gre dla konkretnej liczby graczy, czy sprawdzamy jak się zachowuje gdy graczy jest mniej i wiecej?

    #CO ANALIZOWAĆ - POMYSŁY:
    # - liczba tur w każdej grze - czy jest ich dużo czy mało
    # - liczba tur w każdej grze - jak bardzo się wacha w zależności od kart
    # - średnia ilość wszystkich ruchów w turze
    # - średnia ilość dozwolonych ruchów w turze
    # - kto wygrywa (może gra jest nie fair i np pierwszy gracz ma łatwiej)
    # - procent wykorzystanych kart (ila kart zostało nieodkrytych) - tylko po co to nam? :P