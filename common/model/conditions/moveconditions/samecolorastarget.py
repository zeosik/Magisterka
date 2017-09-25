from common.model.conditions.moveconditions.movecondition import MoveCondition
from common.model.places.place import Place

class SameColorAsTarget(MoveCondition):

    def __init__(self):
        super().__init__('cards have to have same color')

    def test(self, source_place: Place, target_place: Place, artifacts: list):
        target_color = target_place.artifacts()[-1].color
        passed = True
        for card in artifacts:
            if card.color != target_color:
                passed = False
        return passed
