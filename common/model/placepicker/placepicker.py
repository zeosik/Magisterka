from common.model.playerchooser.playerchooser import PlayerChooser
from common.model.places.place import Place
from common.model.playerinput import PlayerInput
from simulator.gamestate import GameState


class PlacePicker(PlayerInput):

    def __init__(self, player_picker: PlayerChooser, place: Place):
        super().__init__('{0}-{1}'.format(player_picker.name, place.name))
        self.place = place
        self.player_picker = player_picker
        self.append_required_inputs(self.player_picker)

    def auto_submitted_values(self, gamestate: GameState) -> list:
        player = self.player_picker.submitted()
        return [gamestate.actual_place(player, self.place)]

    def submitted(self) -> Place:
        return super().submitted()
