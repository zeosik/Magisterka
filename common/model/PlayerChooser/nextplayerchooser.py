from common.model.PlayerChooser.playerchooser import PlayerChooser
from common.model.player import Player
from simulator.gamestate import GameState


class StepPlayerChooser(PlayerChooser):
    def __init__(self, other: PlayerChooser, step: int, name = 'step player chooser'):
        super().__init__(name)
        self.other = other
        self.step = step

    def player(self, gamestate: GameState) -> Player:
        player = self.other.player(gamestate)
        all_players = gamestate.players_for_type(player.type)
        index = all_players.index(player)
        new_index = (index + self.step) % len(all_players)
        return all_players[new_index]


class NextPlayerChooser(StepPlayerChooser):
    def __init__(self, other: PlayerChooser):
        super().__init__(other, 1, 'next-player chooser')


class PreviousPlayerChooser(StepPlayerChooser):
    def __init__(self, other: PlayerChooser):
        super().__init__(other, -1, 'prev-player chooser')