import logging
import gi
from math import pi


from graph_tool import Graph
from graph_tool.draw import sfdp_layout, GraphWidget

from common.model.gamemodel import GameModel
from common.model.phase import Phase
from common.model.playerchooser.playerchooser import PlayerChooser
from common.model.playertype import PlayerType
from common.model.rules.changephase import ChangePhase
from common.model.rules.foreachplayer import ForEachPlayer
from common.model.rules.ifrule import If
from common.model.rules.rule import Rule
from editor.widgets.special.gameflowwidget import GameFlowWidget
from editor.widgets.special.phaseflowwidget import PhaseFlowWidget
from editor.widgets.special.placemapwidget import PlaceMapWidget
from editor.windows.tmputils import TMPUTILS

gi.require_version('Gtk', '3.0')
from gi.repository import Gio, Gtk, Gdk

from example import example_5_10_15


class ViewModelWindow(Gtk.ApplicationWindow):
    def __init__(self, app, show_start_window):
        super().__init__(title='View Model', application=app)
        self.log = logging.getLogger(self.__class__.__name__)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_size_request(1000, 600)
        self.player_types_panel = Gtk.VBox()
        self.main_panel = Gtk.HBox()

        start_button = Gtk.Button('<- Start')
        start_button.connect('clicked', lambda w: show_start_window())

        self.model = None

        self.buttons_panel = Gtk.VBox()
        self.buttons_panel.pack_start(start_button, False, False, 0)

        box = self.box_with_label('start color', TMPUTILS.start_rule_color())
        self.buttons_panel.pack_start(box, False, False, 0)

        box = self.box_with_label('rule color', TMPUTILS.rule_color())
        self.buttons_panel.pack_start(box, False, False, 0)

        self.buttons_panel.pack_start(self.player_types_panel, False, False, 15)
        self.main_panel.pack_start(self.buttons_panel, False, False, 0)


        self.game_flow = GameFlowWidget()
        self.game_flow.set_size_request(100, 100)
        self.game_and_place = Gtk.HPaned()
        self.game_and_place.add1(self.game_flow)

        self.place_map = PlaceMapWidget()
        self.place_map.set_size_request(100, 100)
        self.game_and_place.add2(self.place_map)

        self.phase_flow = PhaseFlowWidget()
        self.phase_flow.set_size_request(100, 100)
        self.flows_panel = Gtk.VPaned()
        self.flows_panel.add1(self.game_and_place)
        self.flows_panel.add2(self.phase_flow)


        self.main_panel.pack_start(self.flows_panel, True, True, 0)
        self.add(self.main_panel)

        self.connect('delete_event', app.on_quit)

    def box_with_label(self, text, color):
        eb = Gtk.EventBox()
        label = Gtk.Label(text)
        eb.add(label)
        eb.modify_bg(Gtk.StateFlags.NORMAL, Gdk.color_parse(color))
        return eb

    def create_player_type_panel(self, player_type: PlayerType, color):
        container = Gtk.VBox()
        box = self.box_with_label(player_type.name, color)
        container.pack_start(box, True, True, 0)
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
        self.phase_flow.draw_for(phase, self.model)

    #def on_vertex_clicked(self, widget, event):
    #    if widget.picked is not None:
    #        name = self.vertex_full_name[widget.picked]
    #        self.phase_name_label.set_text(name)
    #    return False

    def show_game_flow(self, model: GameModel):

        self.clear_container(self.phase_panel)

        all_phases = [phase for pt in [model.table_type] + model.player_types for phase in pt.phases]
        phase_phase = { }
        for phase in all_phases:
            phase_phase[phase] = list(self.end_phases(phase))

        graph = Graph()
        graph.vp.name = graph.new_vertex_property('string')
        graph.vp.color = graph.new_vertex_property('string')
        graph.vp.text_pos = graph.new_vertex_property('float')
        graph.vp.text_off = graph.new_vertex_property('vector<float>')
        phase_vertex = {}
        for phase in all_phases:
            vertex = graph.add_vertex()
            phase_vertex[phase] = vertex
            text = phase.name
            graph.vp.name[vertex] = text
            if phase is model.start_phase:
                color = self.start_rule_color()
            elif phase in model.table_type.phases:
                color = self.table_color()
            else:
                color = self.player_color()
            graph.vp.color[vertex] = color
            graph.vp.text_pos[vertex] = 0
            graph.vp.text_off[vertex] = [0, 0]

        for phase in all_phases:
            for other in phase_phase[phase]:
                graph.add_edge(phase_vertex[phase], phase_vertex[other])

        pos = sfdp_layout(graph)

        vprops = {
            'text': graph.vp.name,
            'fill_color': graph.vp.color,
            'text_position': graph.vp.text_pos,
            'text_offset': graph.vp.text_off
        }

        graph_widget = GraphWidget(graph, pos, vprops=vprops, vertex_size=50)
        self.phase_panel.pack_start(Gtk.Label('gameflow'), False, False, 0)
        self.phase_panel.pack_start(graph_widget, True, True, 0)
        self.phase_panel.show_all()

    def show_model(self, model: GameModel):
        TMPUTILS.clear_container(self.player_types_panel)
        for player_type in [model.table_type] + model.player_types:
            color = TMPUTILS.table_color() if model.table_type is player_type else TMPUTILS.player_color()
            panel = self.create_player_type_panel(player_type, color)
            self.player_types_panel.pack_start(panel, True, True, 0)
        self.model = model
        self.game_flow.draw_for(model)
        self.place_map.draw_for(model)
        self.phase_flow.draw_for(model.start_phase, model)
        #self.show_game_flow(model)
