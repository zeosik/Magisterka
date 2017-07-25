import logging
from gi.overrides.Gtk import Gtk

from common.model.gamemodel import GameModel
from editor.widgets.itemspanel.itemspanel import ItemsPanel
from example import example_5_10_15, example_card_sequence


class StartWindow(Gtk.ApplicationWindow):
    def __init__(self, app, on_game_model_select):
        super().__init__(title='Start', application= app)
        self.log = logging.getLogger(self.__class__.__name__)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_size_request(600, 480)
        self.connect('delete_event', app.on_quit)
        self.on_game_model_select = on_game_model_select

        self.panel = Gtk.VBox()

        for wariant_name, games in self.game_examples().items():
            panel = ItemsPanel(wariant_name, None, self.on_example_select)

            for game_name, game in games.items():
                panel.list_box.add_item(game, game_name)
            self.panel.pack_start(panel, True, True, 0)

        self.add(self.panel)

    def game_examples(self) -> dict:
        games_5_10_15 = {
            '1 faza': example_5_10_15(True),
            '2 fazy': example_5_10_15(False)
        }
        games_two_paies = {
            'standard': example_card_sequence()
        }
        return {
            '5-10-15': games_5_10_15,
            'komplet kart': games_two_paies
        }

    def on_example_select(self, sender, game_model: GameModel):
        self.on_game_model_select(game_model)
