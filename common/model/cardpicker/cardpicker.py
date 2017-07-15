from typing import Tuple

from common.model.PlayerInput import PlayerInput
from common.model.conditions.moveconditions.movecondition import MoveCondition
from common.model.placepicker.placepicker import PlacePicker
from common.model.places.place import Place
from simulator.gamestate import GameState


class CardPicker(PlayerInput):

    def __init__(self, source_place_picker: PlacePicker, target_place_picker: PlacePicker, condition: MoveCondition, name = 'Card Picker'):
        super().__init__(name)
        self.source_place_picker = source_place_picker
        self.target_place_picker = target_place_picker
        self.condition = condition

        self.append_required_inputs(self.source_place_picker)
        self.append_required_inputs(self.target_place_picker)

    def all_choices(self, gamestate: GameState):
        place = self.source_place_picker.submitted()
        return place.artifacts

    def submit_choices(self, choices: list) -> Tuple[bool, str]:
        from_place = self.source_place_picker.submitted()
        to_place = self.target_place_picker.submitted()
        if not self.condition.test(from_place, to_place, choices):
            return False, 'did not match condition: {0}'.format(self.condition.name)
        return super().submit_choices(choices)

    def cards(self, place: Place) -> []:
        pass
