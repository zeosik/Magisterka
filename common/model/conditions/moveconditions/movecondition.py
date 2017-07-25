from common.model.places.place import Place


class MoveCondition:

    def __init__(self, name):
        self.name = name

    def test(self, source_place: Place, target_place: Place, artifacts: list) -> bool:
        pass
