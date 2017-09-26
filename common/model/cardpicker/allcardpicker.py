from common.model.cardpicker.cardpicker import CardPicker
from common.model.conditions.moveconditions.movecondition import MoveCondition
from common.model.placepicker.placepicker import PlacePicker
from simulator.gamestate import GameState

class AllCardPicker(CardPicker):

    def __init__(self, source_place_picker: PlacePicker, target_place_picker: PlacePicker, name = 'All card picker'):
        super().__init__(source_place_picker, target_place_picker, name)

    def simple_name(self):
        return 'All'

    def auto_submitted_values(self, gamestate: GameState) -> list:
        place = self.source_place_picker.submitted()
        return place.artifacts()
