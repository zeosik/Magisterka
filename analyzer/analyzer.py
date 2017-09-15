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
            line_splited = line.split() 
            weight_vector[line_splited[0]] = line_splited[1:]
        config_file.close()

        overal_scores = [0, 0, 0]
        for p_name, parameter in sorted(self.analyzers[0].parameters.items()):
            result = parameter.aggregate(self.analyzers)
            for item in result: # może być kilka wyników z jednego parametru (np średnia i wariancja)
                try:
                    x = item[1]
                    scores = [0, 0, 0]
                    for i in range(3):
                        scores[i] = max(eval(weight_vector[item[0]][i]), 0)
                        overal_scores[i] += scores[i]
                except (KeyError):
                    print("ERROR: W pliku parameter_values.txt nie ma wagi dla parametru", item[0])
                    return
                except:
                    print("ERROR: Sprawdz czy wagi w pliku parameter_values.txt sa dobrze zdefiniowane dla", item[0])
                    return
                print(item[0])
                print("  wartosc:", item[1])
                print("  punkty - 6 lat:", scores[0])
                print("  punkty - 8 lat:", scores[1])
                print("  punkty - 10 lat:", scores[2])
        
        print("Wynik ogolny - 6 lat: ", overal_scores[0])
        print("Wynik ogolny - 8 lat: ", overal_scores[1])
        print("Wynik ogolny - 10 lat: ", overal_scores[2])

def run(game_name, num_players, num_random_bots, num_simulations):
    analysis_aggregator = AnalysisAggregator()

    for n in range(num_simulations):
        print("Iteracja:", n + 1, "/", num_simulations)
        analyzer = simulatorengine.run(game_name, num_players, 0, num_random_bots, True)
        analysis_aggregator.add_analyzer(analyzer)

    analysis_aggregator.print_final_result()

    #Analizujemy gre dla konkretnej liczby graczy, czy sprawdzamy jak się zachowuje gdy graczy jest mniej i wiecej?