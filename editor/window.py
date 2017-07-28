import sys

import gi
import logging

from common.model.gamemodel import GameModel
from editor.windows.phaseflowwindow import PhaseFlowWindow
from editor.windows.placemapwindow import PlaceMapWindow
from editor.windows.startwindow import StartWindow
from editor.windows.viewmodelwindow import ViewModelWindow
from example import example_5_10_15

gi.require_version('Gtk', '3.0')
from gi.repository import Gio, Gtk

from editor.widgets.special.playerswidget import PlayersWidget
from editor.widgets.special.phaseswidget import PhasesWidget
from editor.widgets.special.propertiespanel import PropertiesPanel
from editor.widgets.special.gamecharts import GameCharts
from editor.mediator import Mediator

MENU_XML="""
<?xml version="1.0" encoding="UTF-8"?>
<interface>
    <menu id="app-menu">
        <section>
        <item>
                <attribute name="action">app.load_example_5_10_15</attribute>
                <attribute name="label" translatable="yes">_Load Example</attribute>
                <attribute name="accel">&lt;Primary&gt;l</attribute>
            </item>
            <item>
                <attribute name="action">app.quit</attribute>
                <attribute name="label" translatable="yes">_Quit</attribute>
                <attribute name="accel">&lt;Primary&gt;q</attribute>
            </item>
        </section>
    </menu>
</interface>
"""

class EditorWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(title='Editor', application=app)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_size_request(800, 600)

        self.mediator = Mediator()

        self.main_HBox = Gtk.HBox()

        self.left_panel = Gtk.VBox()
        self.players_widget = PlayersWidget(self.mediator)
        self.left_panel.pack_start(self.players_widget, True, True, 0)
        self.phases_widget = PhasesWidget(self.mediator)
        self.left_panel.pack_start(self.phases_widget, True, True, 0)

        self.main_HBox.pack_start(self.left_panel, True, True, 0)
        self.main_HBox.pack_start(GameCharts(self.mediator), True, True, 0)
        self.main_HBox.pack_start(PropertiesPanel(), True, True, 0)

        self.add(self.main_HBox)

        self.connect('delete_event', app.on_quit)

    def load_model(self, model : GameModel):
        self.mediator.clear_state.fire(self, None)

        for player_type in model.player_types:
            self.mediator.player_types.add.fire(self, player_type)


class EditorApplication(Gtk.Application):
    def __init__(self):
        super().__init__()
        self.log = logging.getLogger(self.__class__.__name__)
        #self.editor_window = None
        self.view_model_window = None
        self.start_window = None
        self.phase_flow_window = None
        self.place_map_window = None

    def do_activate(self):
        #self.editor_window = EditorWindow(self)
        self.phase_flow_window = PhaseFlowWindow(self)
        self.view_model_window = ViewModelWindow(self, self.show_start_window, self.phase_flow_window.draw_for)
        self.start_window = StartWindow(self, self.show_game_model)
        self.place_map_window = PlaceMapWindow(self)
        self.show_start_window()

    def do_startup(self):
        Gtk.Application.do_startup(self)

        action = Gio.SimpleAction.new('quit', None)
        action.connect('activate', self.on_quit)
        self.add_action(action)

        action2 = Gio.SimpleAction.new('load_example_5_10_15', None)
        action2.connect('activate', self.load_example_5_10_15)
        self.add_action(action2)

        builder = Gtk.Builder.new_from_string(MENU_XML, -1)
        self.set_app_menu(builder.get_object('app-menu'))

    def on_quit(self, action, param):
        self.quit()

    def show_game_model(self, model: GameModel):
        self.start_window.hide()
        self.view_model_window.show_model(model)
        self.view_model_window.show_all()

        self.phase_flow_window.draw_for(model.start_phase, model)
        self.phase_flow_window.show_all()

        self.place_map_window.draw_for(model)
        self.place_map_window.show_all()

    def show_start_window(self):
        self.start_window.show_all()
        self.view_model_window.hide()
        #self.editor_window.hide()


    def load_example_5_10_15(self, action, param):
        self.log.debug('loading example')
        model = example_5_10_15(False)
        #self.editor_window.load_model(model)
        #self.editor_window.hide()

        self.view_model_window.show_model(model)
        self.view_model_window.show_all()


def run():
    app = EditorApplication()
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)
