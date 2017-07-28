import gi
import logging

from graph_tool import Graph
from graph_tool.draw import GraphWidget, sfdp_layout

from common.model.gamemodel import GameModel
from editor.windows.tmputils import TMPUTILS

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class GameFlowWidget(Gtk.VBox):

    def __init__(self):
        super().__init__()
        self.log = logging.getLogger(self.__class__.__name__)

        self.add(Gtk.Label(self.__class__.__name__))

    def draw_for(self, model: GameModel):
        self.log.debug('drawing game flow for model {0}'.format(model.name))
        for child in self.get_children():
            self.remove(child)

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
        self.pack_start(Gtk.Label('gameflow'), False, False, 0)
        self.pack_start(graph_widget, True, True, 0)
        #self.show_all()
