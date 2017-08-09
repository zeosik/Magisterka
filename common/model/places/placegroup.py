import copy

import logging

from common.model.places.place import Place


class PlaceGroup(Place):

    def __init__(self, template_place: Place):
        #self.log = logging.getLogger(self.__class__.__name__)
        super().__init__("PlaceGroup {0}".format(template_place.name))
        self._template_place = template_place
        self.places = []
        self.new_place_counter = 1

    #TODO moze to wrzucic do Place i zmienic nazwe?
    def get_cards(self, player=None):
        return [c for place in self.places for c in place.get_cards(player)]

    def add_new(self):
        new_place = copy.deepcopy(self._template_place)
        new_place.set_player(self.player)
        new_place.name = "#{0}-{1}".format(self.new_place_counter, self._template_place.name)
        self.new_place_counter += 1
        self.places.append(new_place)

    #mozemy użyc grupy miejsc jako miejsca, bo czemu nie
    def artifacts(self):
        return [a for place in self.places for a in place.artifacts()]

    def remove_artifact(self, artifact):
        for place in self.places:
            if artifact in place.artifacts():
                place.remove_artifact(artifact)

    def add_artifact(self, artifact):
        #self.log.error('not supported operation, specify a place ')
        raise Exception()
