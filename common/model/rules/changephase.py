from common.model.phase import Phase
from common.model.rules.rule import Rule


class ChangePhase(Rule):
    def __init__(self, to_phase:Phase, player):
        super().__init__('Change phase to: {0} {1}'.format(to_phase.name, player.enum.name))
        self.phase = to_phase
        self.player = player
