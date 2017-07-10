from common.model.phase import Phase
from common.model.rules.rule import Rule

class WinCheck(Rule):
    def __init__(self, next_phase:Phase, win_phase:Phase):
        super().__init__('Check for win')
        self.counter = 3    #symuluje rozgrywke i to, ze w pewnym momencie ktoś wygra
        self.phase = next_phase
        self.win_phase = win_phase

    def apply(self, gamestate):
        #TODO przekazać do WinCheck coś co będzie liczyć punkty
        self.counter -= 1
        if self.counter == 0:
            self.phase = self.win_phase
