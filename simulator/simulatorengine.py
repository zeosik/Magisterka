from example import example_5_10_15
from common.model.phase import Phase

class SimulatorEngine():
    def __init__(self, game_function, debug = True):
        self.game = game_function()
        self.debug = debug
        
    def log(self, msg):
        if self.debug:
            print(msg)

    def run(self):
        self.log("Uruchamiam symulacje gry: " + self.game.name)

        current_phase = self.game.start_phase

        while current_phase != self.game.end_phase:
            self.log("-Przechodze do fazy: " + current_phase.name)

            for rule in current_phase.rules:
                ret = rule()
                self.log("--Przetwarzam regule: " + rule.__name__)

                if type(ret) is Phase:
                    current_phase = ret
        else:
            self.log("-Przechodze do fazy: " + current_phase.name)        

        self.log("Koncze symulacje")

def run():
    engine = SimulatorEngine(lambda: example_5_10_15())
    engine.run()