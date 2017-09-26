from typing import Tuple

from common.model.playerinput import PlayerInput
from common.model.conditions.moveconditions.movecondition import MoveCondition
from common.model.placepicker.placepicker import PlacePicker
from common.model.places.place import Place
from simulator.gamestate import GameState


class CardPicker(PlayerInput):

    def __init__(self, source_place_picker: PlacePicker, target_place_picker: PlacePicker, name: str = 'Card Picker'):
        super().__init__('{0} from: {1}, to: {2}'.format(name, source_place_picker.name, target_place_picker.name))
        self.source_place_picker = source_place_picker
        self.target_place_picker = target_place_picker
        self.conditions = []
        self.append_required_inputs(self.source_place_picker)
        self.append_required_inputs(self.target_place_picker)

    def simple_name(self) -> str:
        return "P"

    def add_condition(self, condition: MoveCondition):
        self.conditions.append(condition)

    def all_choices(self, gamestate: GameState):
        place = self.source_place_picker.submitted()
        return place.artifacts()

    def submit_choices(self, choices: list) -> Tuple[bool, str]:
        from_place = self.source_place_picker.submitted()
        to_place = self.target_place_picker.submitted()
        for condition in self.conditions:
            if not condition.test(from_place, to_place, choices):
                return False, 'did not match condition: {0}'.format(condition.name)
        return super().submit_choices(choices)

