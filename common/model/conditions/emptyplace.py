from common.model.conditions.artifactsinplaceequal import ArtifactsInPlaceEqual
from common.model.conditions.ifcondition import IfCondition
from common.model.placepicker.placepicker import PlacePicker
from simulator.gamestate import GameState


class EmptyPlace(ArtifactsInPlaceEqual):

    def __init__(self, place_picker: PlacePicker):
        super().__init__(0, place_picker)
