from common.model.cardpicker.cardpicker import CardPicker
from common.model.conditions.moveconditions.movecondition import MoveCondition
from common.model.placepicker.placepicker import PlacePicker
from simulator.gamestate import GameState

class TopCardPicker(CardPicker):

    def __init__(self, card_count, source_place_picker: PlacePicker, target_place_picker: PlacePicker, condition: MoveCondition = MoveCondition()):
        super().__init__(source_place_picker, target_place_picker, condition, 'Top card picker')
        self.card_count = card_count

    def auto_submitted_values(self, gamestate: GameState) -> list:
        place = self.source_place_picker.submitted()
        # TODO przemyśleć czy kolejność ma tutaj znaczenie? (czy dobieramy na raz, czy po jednej?)
        return place.artifacts[-self.card_count:]
