import logging

import collections
import gi

from editor.mediator import Mediator

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from common.model.gamemodel import GameModel
from editor.widgets.itemspanel.itemspanel import ItemsPanel
from example import *


class StartWindow(Gtk.ApplicationWindow):
    def __init__(self, app, mediator: Mediator):
        super().__init__(title='Start', application= app)
        self.log = logging.getLogger(self.__class__.__name__)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_size_request(600, 480)
        self.connect('delete_event', app.on_quit)
        self.mediator = mediator
        self.mediator.model_select.register(self.hide_widnow)

        self.panel = Gtk.VBox()

        for wariant_name, games in self.game_examples().items():
            panel = ItemsPanel(wariant_name, None, self.mediator.model_select.fire)

            for game_name, game in games.items():
                panel.list_box.add_item(game, game_name)
            self.panel.pack_start(panel, True, True, 0)

        self.add(self.panel)

    def hide_widnow(self, sender, obj):
        self.hide()

    def game_examples(self) -> dict:
        games_5_10_15 = {
            '1 faza': example_5_10_15(True),
            '2 fazy': example_5_10_15(False),
            #test
            'test':test()
        }
        games_two_paies = {
            'standard': example_card_sequence()
        }
        games_remik = {
            'standard': example_remik()
        }
        games = collections.OrderedDict()
        games['5-10-15'] = games_5_10_15
        games['komplet kart'] = games_two_paies
        games['remik'] =  games_remik
        return games
