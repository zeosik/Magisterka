from common.model.playerchooser.playerchooser import PlayerChooser
from common.model.places.place import Place
from common.model.playerinput import PlayerInput
from simulator.gamestate import GameState


class PlacePicker(PlayerInput):

    def __init__(self, playerpicker: PlayerChooser, place: Place):
        super().__init__('Place Picker place: {0}, player: {1}'.format(place.name, playerpicker.name))
        self.place = place
        self.player_picker = playerpicker
        self.append_required_inputs(self.player_picker)

    def auto_submitted_values(self, gamestate: GameState) -> list:
        player = self.player_picker.submitted()
        return [gamestate.actual_place(player, self.place)]
