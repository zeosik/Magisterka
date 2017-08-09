import logging

from common.model.placepicker.placepicker import PlacePicker
from common.model.places.place import Place
from common.model.places.placegroup import PlaceGroup
from common.model.playerchooser.playerchooser import PlayerChooser
from simulator.gamestate import GameState


class LastGroupPlacePicker(PlacePicker):
    def __init__(self, player_picker: PlayerChooser, place: PlaceGroup):
        super().__init__(player_picker, place)
        self.log = logging.getLogger(self.__class__.__name__)

    def auto_submitted_values(self, gamestate: GameState):
        groups = super().auto_submitted_values(gamestate)
        if len(groups) != 1:
            self.log.error('expected single place group')
            raise Exception()
        place_group = groups[0]
        if len( place_group.places) < 1:
            self.log.error('no places')
        return [place_group.places[-1]]
