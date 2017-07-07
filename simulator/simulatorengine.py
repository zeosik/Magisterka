import logging

from example import example_5_10_15
from common.model.phase import Phase

class SimulatorEngine():
    def __init__(self, game):
        self.log = logging.getLogger(self.__class__.__name__)
        self.game = game

    def run(self):
        self.log.debug("Uruchamiam symulacje gry: " + self.game.name)

        current_phase = self.game.start_phase

        while current_phase != self.game.end_phase:
            self.log.debug("-Przechodze do fazy: " + current_phase.name)

            for rule in current_phase.rules:
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