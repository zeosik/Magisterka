from typing import Callable

from common.model.conditions.ifcondition import IfCondition
from common.model.placepicker.placepicker import PlacePicker
from simulator.gamestate import GameState


class ArtifactsInPlace(IfCondition):

    def __init__(self, number:int ,  place_picker: PlacePicker, comparator: Callable[[int, int], bool], name):
        super().__init__(name)
        self.number = number
        self.place_picker = place_picker
        self.comparator = comparator

    def evaluate(self, gamestate: GameState):
        #TODO trza cos z tym bedzie zrobic ale teraz mozna sobie zagrac :P
        for i in self.place_picker.required_inputs():
            i.requires_player_input(gamestate)
        self.place_picker.requires_player_input(gamestate)
        place = self.place_picker.submitted()
        return self.comparator(len(place.artifacts), self.number)
