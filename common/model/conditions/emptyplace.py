from common.model.conditions.ifcondition import IfCondition
from common.model.placepicker.placepicker import PlacePicker
from simulator.gamestate import GameState


class EmptyPlace(IfCondition):

    def __init__(self, place_picker: PlacePicker):
        super().__init__('empty stack')
        self.place_picker = place_picker

    def evaluate(self, gamestate: GameState):
        #TODO trza cos z tym bedzie zrobic ale teraz mozna sobie zagrac :P
        for i in self.place_picker.required_inputs():
            i.requires_player_input(gamestate)
        self.place_picker.requires_player_input(gamestate)
        place = self.place_picker.submitted()
        return len(place.artifacts) == 0
