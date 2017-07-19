from common.model.playerinput import PlayerInput
from common.model.player import Player


class PlayerChooser(PlayerInput):

    def __init__(self, name):
        super().__init__(name)

    def submitted(self) -> Player:
        return super().submitted()
