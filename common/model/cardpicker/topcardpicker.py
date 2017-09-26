import logging

from common.model.cardpicker.cardpicker import CardPicker
from common.model.placepicker.placepicker import PlacePicker
from simulator.gamestate import GameState

class TopCardPicker(CardPicker):

    def __init__(self, card_count, source_place_picker: PlacePicker, target_place_picker: PlacePicker, name = 'Top card picker'):
        super().__init__(source_place_picker, target_place_picker, name)
        self.log = logging.getLogger(self.__class__.__name__)
        self.card_count = card_count

    def simple_name(self):
        return "T({0})".format(self.card_count)

    def auto_submitted_values(self, gamestate: GameState) -> list:
        place = self.source_place_picker.submitted()
        # TODO przemyśleć czy kolejność ma tutaj znaczenie? (czy dobieramy na raz, czy po jednej?)
        if len(place.artifacts()) < self.card_count:
            self.log.error('not enough artifacts in place {0} size {1} to pick, required {2}'.format(place.name, len(place.artifacts()), self.card_count))
            # TODO moze jakis wlasny exception :P
            raise Exception()
        return place.artifacts()[-self.card_count:]
