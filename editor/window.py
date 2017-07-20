import sys

import gi
import logging

from graph_tool import Graph
from graph_tool.draw import GraphWidget, sfdp_layout

from common.model.gamemodel import GameModel
from common.model.phase import Phase
from common.model.playertype import PlayerType
from common.model.rules.changephase import ChangePhase
from common.model.rules.ifrule import If
from common.model.rules.rule import Rule
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
        Gtk.ApplicationWindow.__init__(self, title='Editor', application=app)
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

    def load_model(self, model : GameModel):
        self.mediator.clear_state.fire(self, None)

        for player_type in model.player_types:
            self.mediator.player_types.add.fire(self, player_type)


class ModelViewWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        Gtk.ApplicationWindow.__init__(self, title='View Model', application=app)
        self.log = logging.getLogger(self.__class__.__name__)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_size_request(1000, 600)
        self.player_types_panel = Gtk.VBox()
        self.main_panel = Gtk.HBox()
        self.phase_panel = Gtk.VBox()
        button = Gtk.Button('game Flow')
        self.model = example_5_10_15()
        button.connect('clicked', lambda w: self.show_game_flow(self.model))
        self.main_panel.pack_start(button, False, False, 0)
        self.main_panel.pack_start(self.player_types_panel, False, False, 0)
        self.main_panel.pack_start(self.phase_panel, True, True, 0)
        self.add(self.main_panel)

    def create_player_type_panel(self, player_type: PlayerType):
        container = Gtk.VBox()
        name = Gtk.Label(player_type.name)
        container.pack_start(name, True, True, 0)
        phases = Gtk.ListBox()
        phases.connect('row-activated', lambda lb, row: self.show_phase(row.object))
        for phase in player_type.phases:
            row = Gtk.ListBoxRow()
            row.add(Gtk.Label(phase.name))
            row.object = phase
            phases.add(row)

        container.pack_start(phases, True, True, 0)
        return container

    def show_phase(self, phase: Phase):
        self.log.debug('showing phase: {0}'.format(phase.name))
        self.clear_container(self.phase_panel)

        name = Gtk.Label(phase.name)
        self.phase_panel.pack_start(name, False, False, 0)

        start = Rule('start {0}'.format(phase.name))
        start.next = phase.rules
        #phase.rules = [start]

        rules = set()
        rules.add(start)
        self.append_rules(rules, start)

        #for rule in rules:
        #    label = Gtk.Label(rule.name[:30])
        #    self.phase_panel.pack_start(label, True, True, 0)

        graph = Graph()
        #graph.vp.pos = graph.new_vertex_property('vector<double>')
        graph.vp.name = graph.new_vertex_property('string')

        rule_vertex = {}

        for rule in rules:
            vertex = graph.add_vertex()
            rule_vertex[rule] = vertex
            graph.vp.name[vertex] = rule.name[:15]

        for rule in rules:
            for next_rule in self.next_rules(rule):
                graph.add_edge(rule_vertex[rule], rule_vertex[next_rule])

        pos = sfdp_layout(graph)

        graph_widget = GraphWidget(graph, pos, vertex_text = graph.vp.name, vertex_font_size=12, vertex_size=10)
        self.phase_panel.pack_start(graph_widget, True, True, 0)

        self.phase_panel.show_all()

    def show_game_flow(self, model: GameModel):

        self.clear_container(self.phase_panel)

        all_phases = [phase for pt in [model.table_type] + model.player_types for phase in pt.phases]
        phase_phase = { }
        for phase in all_phases:
            phase_phase[phase] = list(self.end_phases(phase))

        graph = Graph()
        graph.vp.name = graph.new_vertex_property('string')
        phase_vertex = {}
        for phase in all_phases:
            vertex = graph.add_vertex()
            phase_vertex[phase] = vertex
            graph.vp.name[vertex] = phase.name

        for phase in all_phases:
            for other in phase_phase[phase]:
                graph.add_edge(phase_vertex[phase], phase_vertex[other])

        pos = sfdp_layout(graph)

        graph_widget = GraphWidget(graph, pos, vertex_text=graph.vp.name, vertex_font_size=12, vertex_size=10)
        self.phase_panel.pack_start(Gtk.Label('gameflow'), False, False, 0)
        self.phase_panel.pack_start(graph_widget, True, True, 0)
        self.phase_panel.show_all()

    def end_phases(self, phase: Phase):
        all_rules = set()
        tmp = Rule('tmp')
        tmp.next = phase.rules
        self.append_rules(all_rules, tmp)
        return set([rule.phase for rule in all_rules if issubclass(rule.__class__, ChangePhase)])

    def show_model(self, model: GameModel):
        self.clear_container(self.player_types_panel)
        for player_type in [model.table_type] + model.player_types:
            panel = self.create_player_type_panel(player_type)
            self.player_types_panel.pack_start(panel, True, True, 0)
        self.model = model
        self.show_game_flow(model)

    def clear_container(self, container):
        for child in container.get_children():
            container.remove(child)

    def append_rules(self, all: set, rule):
        for r in self.next_rules(rule):
            if r not in all:
                all.add(r)
                self.append_rules(all, r)

    #taki cheat
    def next_rules(self, rule) -> list:
        if issubclass(rule.__class__, If):
            return rule.if_true + rule.if_false
        else:
            return rule.next

class EditorApplication(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self)
        self.log = logging.getLogger(self.__class__.__name__)
        self.editor_window = None
        self.view_model_window = None

    def do_activate(self):
        self.editor_window = EditorWindow(self)
        self.view_model_window = ModelViewWindow(self)
        self.editor_window.show_all()

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

    def load_example_5_10_15(self, action, param):
        self.log.debug('loading example')
        model = example_5_10_15()
        self.editor_window.load_model(model)
        self.editor_window.hide()

        self.view_model_window.show_model(model)
        self.view_model_window.show_all()


def run():
    app = EditorApplication()
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)
