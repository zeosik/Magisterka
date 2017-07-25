from common.model.cardpicker.topcardpicker import TopCardPicker
from common.model.placepicker.placepicker import PlacePicker
from simulator.gamestate import GameState


class TopCardFillPicker(TopCardPicker):

    def __init__(self, fill_to_card_count, source_place_picker: PlacePicker, target_place_picker: PlacePicker):
        super().__init__(fill_to_card_count, source_place_picker, target_place_picker, name='Top Card Fill Picker')
        self.fill_to_card_count = fill_to_card_count

    def auto_submitted_values(self, gamestate: GameState):
        to_place = self.target_place_picker.submitted()
        self.card_count = self.fill_to_card_count - len(to_place.artifacts)
        if self.card_count > 0:
            return super().auto_submitted_values(gamestate)
        return []
