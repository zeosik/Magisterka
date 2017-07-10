from common.model.phase import Phase
from common.model.places.place import Place


class PlayerType:

    def __init__(self, name):
        self.name = name
        self.phases = []
        self.places = []

    def add_phase(self, phase: Phase) -> Phase:
        self.phases.append(phase)
        return phase

    def add_place(self, place: Place) -> Place:
        self.places.append(place)
        return place
