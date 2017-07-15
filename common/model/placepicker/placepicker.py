from common.model.PlayerChooser.playerchooser import PlayerChooser
from common.model.PlayerInput import PlayerInput
from common.model.places.place import Place
from simulator.gamestate import GameState


class PlacePicker(PlayerInput):

    def __init__(self, playerpicker: PlayerChooser, place: Place):
        super().__init__('place picker')
        self.player_picker = playerpicker
        self.place = place

        self.append_required_inputs(self.player_picker)

    def auto_submitted_values(self, gamestate: GameState) -> list:
        player = self.player_picker.submitted()
        return [gamestate.actual_place(player, self.place)]
