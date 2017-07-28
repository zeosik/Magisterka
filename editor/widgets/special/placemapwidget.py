import gi
import logging

from common.model.gamemodel import GameModel

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class PlaceMapWidget(Gtk.VBox):

    def __init__(self):
        super().__init__()
        self.log = logging.getLogger(self.__class__.__name__)

        self.add(Gtk.Label(self.__class__.__name__))

    def draw_for(self, model: GameModel):
        self.log.debug('drawing place map for model {0}'.format(model.name))
        for child in self.get_children():
            self.remove(child)

