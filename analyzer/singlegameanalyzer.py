from analyzer.parameters.playerphasecounter import PlayerPhaseCounter
from analyzer.parameters.winerfairnesschecker import WinerFairnessChecker
from analyzer.parameters.cardusagechecker import CardUsageChecker

class SingleGameAnalyzer:
    def __init__(self):
        self.parameters = dict()
        self.parameters["PlayerPhaseCounter"] = PlayerPhaseCounter()
        self.parameters["WinerFairnessChecker"] = WinerFairnessChecker()
        self.parameters["CardUsageChecker"] = CardUsageChecker()

    # Wywoływane co ruch
    def run_analysis(self, gamestate):
        self.parameters["PlayerPhaseCounter"].run(gamestate)

    # Wywoływane raz na koniec gry
    def run_end_game_analysis(self, gamestate):
        self.parameters["WinerFairnessChecker"].run(gamestate)
        self.parameters["CardUsageChecker"].run(gamestate)