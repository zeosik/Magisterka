import logging

import gi
from graph_tool import Graph
from graph_tool.draw import sfdp_layout, GraphWidget

from common.model.gamemodel import GameModel
from common.model.playertype import PlayerType
from editor.windows.tmputils import TMPUTILS

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


class ViewModelWindow(Gtk.ApplicationWindow):
    def __init__(self, app, show_start_window, show_phase):
        super().__init__(title='View Model', application=app)
        self.log = logging.getLogger(self.__class__.__name__)
        #self.set_position(Gtk.WindowPosition.CENTER)
        self.set_size_request(800, 400)
        self.move(0, 500)
        self.player_types_panel = Gtk.VBox()
        self.main_panel = Gtk.HBox()
        self.show_phase = show_phase

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

        self.game_flow_panel = Gtk.VBox()
        self.main_panel.pack_start(self.game_flow_panel, True, True, 0)

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
        phases.connect('row-activated', lambda lb, row: self.show_phase(row.object, self.model))
        for phase in player_type.phases:
            row = Gtk.ListBoxRow()
            row.add(Gtk.Label(phase.name))
            row.object = phase
            phases.add(row)

        container.pack_start(phases, True, True, 0)
        return container

    def show_model(self, model: GameModel):
        TMPUTILS.clear_container(self.player_types_panel)
        for player_type in [model.table_type] + model.player_types:
            color = TMPUTILS.table_color() if model.table_type is player_type else TMPUTILS.player_color()
            panel = self.create_player_type_panel(player_type, color)
            self.player_types_panel.pack_start(panel, True, True, 0)
        self.model = model
        self.draw_game_flow(model)

    def draw_game_flow(self, model: GameModel):
        self.log.debug('drawing game flow for model {0}'.format(model.name))
        TMPUTILS.clear_container(self.game_flow_panel)

        all_phases = [phase for pt in [model.table_type] + model.player_types for phase in pt.phases]
        phase_phase = {}
        for phase in all_phases:
            phase_phase[phase] = list(TMPUTILS.end_phases(phase))

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
                color = TMPUTILS.start_rule_color()
            elif phase in model.table_type.phases:
                color = TMPUTILS.table_color()
            else:
                color = TMPUTILS.player_color()
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
        self.game_flow_panel.pack_start(Gtk.Label('gameflow'), False, False, 0)
        self.game_flow_panel.pack_start(graph_widget, True, True, 0)
        #self.show_all()

