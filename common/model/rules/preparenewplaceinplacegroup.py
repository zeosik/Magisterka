from common.model.placepicker.placepicker import PlacePicker
from common.model.rules.rule import Rule
from simulator.gamestate import GameState


class PrepareNewPlaceInPlaceGroup(Rule):
    def __init__(self, place_picker: PlacePicker):
        super().__init__('new place {0}'.format(place_picker.name))
        self.place_picker = place_picker
        self.register_input(self.place_picker)

    def apply(self, gamestate: GameState):
        place_group = self.place_picker.submitted()
        place_group.add_new()
