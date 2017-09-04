from analyzer.parameters.parameter import Parameter

class WinerFairnessChecker(Parameter):
    def __init__(self):
        super().__init__("WinerFairnessChecker")
        self.winner_name = None
        self.num_players = None
        
    def run(self, gamestate):
        self.winner_name = gamestate.current_player_for_type(gamestate.model.player_types[0]).name
        self.num_players = gamestate.number_of_players()

    def result(self):
        return (self.winner_name, self.num_players)

    def aggregate(self, analyzers):
        # TODO tu trzeba jakoś ładnie to wypisać (z uwzgdlędnieniem liczby graczy)
        winers = dict()
        for a in analyzers:
            single_result = a.parameters[self.name].result()
            if single_result[0] in winers:
                winers[single_result[0]] += 1
            else:
                winers[single_result[0]] = 1
        return [(self.name, str(winers))]
