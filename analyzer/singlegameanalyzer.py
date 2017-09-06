from analyzer.parameters.playerphasecounter import PlayerPhaseCounter
from analyzer.parameters.numberofmovescounter import NumberOfMovesCounter
from analyzer.parameters.winerfairnesschecker import WinerFairnessChecker
from analyzer.parameters.cardusagechecker import CardUsageChecker

class SingleGameAnalyzer:
    def __init__(self):
        self.parameters = dict()
        self.parameters["PlayerPhaseCounter"] = PlayerPhaseCounter()
        self.parameters["NumberOfMovesCounter"] = NumberOfMovesCounter()
        self.parameters["WinerFairnessChecker"] = WinerFairnessChecker()
        self.parameters["CardUsageChecker"] = CardUsageChecker()

    # Wywoływane co ruch
    def run_analysis(self, gamestate, rule_picker):
        self.parameters["PlayerPhaseCounter"].run(gamestate)
        self.parameters["NumberOfMovesCounter"].run(gamestate, rule_picker)

    # Wywoływane raz na koniec gry
    def run_end_game_analysis(self, gamestate):
        self.parameters["WinerFairnessChecker"].run(gamestate)
        self.parameters["CardUsageChecker"].run(gamestate)