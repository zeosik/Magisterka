from analyzer.parameters.playerphasecounter import PlayerPhaseCounter

class SingleGameAnalyzer:
    def __init__(self):
        self.parameters = []
        self.parameters.append(PlayerPhaseCounter())

    def run_analysis(self, gamestate):
        for p in self.parameters:
            p.run(gamestate)