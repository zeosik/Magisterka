from common.model.conditions.moveconditions.movecondition import MoveCondition
from common.model.places.place import Place


class NumberOfMovedArtifacts(MoveCondition):

    def __init__(self, number: int):
        super().__init__('Number of artifacts must be: {0}'.format(number))
        self.number = number

    def test(self, source_place: Place, target_place: Place, artifacts: list):
        return len(artifacts) == self.number
