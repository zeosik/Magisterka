import logging

from common.model.gamemodel import GameModel
from common.model.rules.changephase import ChangePhase
from common.model.rules.rule import Rule
from example import example_5_10_15
from common.model.phase import Phase

class SimulatorEngine():
    def __init__(self, game: GameModel):
        self.log = logging.getLogger(self.__class__.__name__)
        self.game = game

    def run(self):
        self.log.debug("Uruchamiam symulacje gry: " + self.game.name)

        current_phase = self.game.start_phase

        while current_phase != self.game.end_phase:
            self.log.debug("-Przechodze do fazy: " + current_phase.name)

            for rule in current_phase.rules:
                if issubclass(rule.__class__, Rule):
                    ret = None
                    self.log.debug("--Przetwarzam regule: " + rule.name)
                    if type(rule) is ChangePhase:
                        current_phase = rule.phase
                else:
                    ret = rule()
                    self.log.debug("--Przetwarzam regule: " + rule.__name__)

                if type(ret) is Phase:
                    current_phase = ret
        else:
            self.log.debug("-Przechodze do fazy: " + current_phase.name)

        self.log.debug("Koncze symulacje")

def run():
    engine = SimulatorEngine(example_5_10_15())
    engine.run()