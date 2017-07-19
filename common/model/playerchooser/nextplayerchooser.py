from common.model.playerchooser.playerchooser import PlayerChooser
from common.model.player import Player
from simulator.gamestate import GameState


class StepPlayerChooser(PlayerChooser):
    def __init__(self, other: PlayerChooser, step: int, name = 'step player chooser'):
        super().__init__(name)
        self.step = step
        self.other = other
        self.append_required_inputs(self.other)

    def auto_submitted_values(self, gamestate: GameState) -> list:
        player = self.other.submitted()
        all_players = gamestate.players_for_type(player.type)
        index = all_players.index(player)
        new_index = (index + self.step) % len(all_players)
        return [all_players[new_index]]


class NextPlayerChooser(StepPlayerChooser):
    def __init__(self, other: PlayerChooser):
        super().__init__(other, 1, 'next-player chooser')


class PreviousPlayerChooser(StepPlayerChooser):
    def __init__(self, other: PlayerChooser):
        super().__init__(other, -1, 'prev-player chooser')