import gi
import logging

from graph_tool import Graph
from graph_tool.draw import sfdp_layout, GraphWidget

from common.model.gamemodel import GameModel
from editor.windows.tmputils import TMPUTILS

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class PlaceMapWindow(Gtk.ApplicationWindow):

    def __init__(self, app):
        super().__init__(title='Place map', application=app)
        self.log = logging.getLogger(self.__class__.__name__)
        self.set_size_request(600, 400)
        self.move(700, 0)
        self.main_panel = Gtk.VBox()
        self.add(self.main_panel)

    def draw_for(self, model: GameModel):
        self.log.debug('drawing place map for model {0}'.format(model.name))
        TMPUTILS.clear_container(self.main_panel)

        all_places = set()
        for player_type in model.player_types + [model.table_type]:
            for place in player_type.places:
                all_places.add(place)

        place_vertex = {}

        graph = Graph()
        graph.vp.name = graph.new_vertex_property('string')
        graph.vp.color = graph.new_vertex_property('string')
        graph.vp.text_pos = graph.new_vertex_property('float')

        for place in all_places:
            vertex = graph.add_vertex()
            place_vertex[place] = vertex

            graph.vp.name[vertex] = place.name
            graph.vp.color[vertex] = TMPUTILS.table_color() if place in model.table_type.places else TMPUTILS.player_color()
            graph.vp.text_pos[vertex] = 0

        pos = sfdp_layout(graph)

        vprops = {
            'text': graph.vp.name,
            'fill_color': graph.vp.color,
            'text_position': graph.vp.text_pos,
        }

        graph_widget = GraphWidget(graph, pos, vprops=vprops, vertex_size=50)
        self.main_panel.pack_start(graph_widget, True, True, 0)
        self.main_panel.show_all()
