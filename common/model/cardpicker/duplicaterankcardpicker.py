from common.model.cardpicker.cardpicker import CardPicker
from common.model.conditions.moveconditions.movecondition import MoveCondition
from common.model.placepicker.placepicker import PlacePicker
from simulator.gamestate import GameState


class DuplicateRankCardPicker(CardPicker):

    def __init__(self, source_place_picker: PlacePicker, target_place_picker: PlacePicker):
        super().__init__(source_place_picker, target_place_picker, 'Duplicate Card Picker')
        #TODO moze jakis artifact comparator i dac CardRankComparator

    def simple_name(self):
        return "Dup"

    def auto_submitted_values(self, gamestate: GameState):
        place = self.source_place_picker.submitted()

        unique_ranks = set()
        duplicates = []
        for x in place.artifacts():
            if x.rank not in unique_ranks:
                unique_ranks.add(x.rank)
            else:
                duplicates.append(x)

        return duplicates