from common.model.conditions.moveconditions.movecondition import MoveCondition
from common.model.places.place import Place


class CardsSumsTo(MoveCondition):

    def __init__(self, sums_to_list: list):
        super().__init__('cards rank sum must be in {0}'.format(sums_to_list))
        self.sums_to_list = sums_to_list

    def test(self, source_place: Place, target_place: Place, artifacts: list):
        return sum([card.rank for card in artifacts]) in self.sums_to_list
