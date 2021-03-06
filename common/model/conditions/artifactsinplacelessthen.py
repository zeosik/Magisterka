from common.model.conditions.artifactsinplace import ArtifactsInPlace
from common.model.placepicker.placepicker import PlacePicker


class ArtifactsInPlaceLessThen(ArtifactsInPlace):

    def __init__(self, number: int, place_picker: PlacePicker):
        super().__init__(number, place_picker, lambda a, b: a < b, 'less then')
