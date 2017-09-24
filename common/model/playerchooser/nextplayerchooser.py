from common.model.playerchooser.playerchooser import PlayerChooser
from common.model.player import Player
from simulator.gamestate import GameState


class StepPlayerChooser(PlayerChooser):
    def __init__(self, other: PlayerChooser, step: int, condition = None, name = 'step player chooser'):
        super().__init__(name)
        self.condition = condition
        self.step = step
        self.other = other
        self.append_required_inputs(self.other)

    def auto_submitted_values(self, gamestate: GameState) -> list:
        player = self.other.submitted()
        all_players = gamestate.players_for_type(player.type)
        index = all_players.index(player)

        new_index = index
        for i in range(abs(self.step)):
            k = 1 if self.step > 0 else -1
            new_index = (new_index + k) % len(all_players)
            while self.condition is not None and self.condition(gamestate, all_players[new_index]):
                new_index = (new_index + k) % len(all_players)

        #new_index = (index + self.step) % len(all_players)
        return [all_players[new_index]]


class NextPlayerChooser(StepPlayerChooser):
    def __init__(self, other: PlayerChooser, condition = None):
        super().__init__(other, 1, condition, 'next {0}'.format(other.name))


class PreviousPlayerChooser(StepPlayerChooser):
    def __init__(self, other: PlayerChooser, condition = None):
        super().__init__(other, -1, condition, 'prev {0}'.format(other.name))