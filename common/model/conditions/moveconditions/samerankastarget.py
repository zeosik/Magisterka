from common.model.conditions.moveconditions.movecondition import MoveCondition
from common.model.places.place import Place

class SameRankAsTarget(MoveCondition):

    def __init__(self):
        super().__init__('cards have to have same rank')

    def test(self, source_place: Place, target_place: Place, artifacts: list):
        target_rank = target_place.artifacts()[-1].rank
        passed = True
        for card in artifacts:
            if card.rank != target_rank:
                passed = False
        return passed
