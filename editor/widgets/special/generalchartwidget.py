import gi
from graph_tool import Graph
from graph_tool.draw import GraphWidget

from editor.widgets.itemspanel.panelheader import PanelHeader
from common.player import Player
from common.phase import Phase
from common.game import Game

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class GeneralChartWidget(Gtk.VBox):

    def __init__(self, mediator):
        Gtk.VBox.__init__(self)

        self.header = PanelHeader('General view')

        self.pack_start(self.header, False, False, 0)

        mediator.register_on_player_add_listener(self.draw_chart)
        mediator.register_on_phase_add_listener(self.draw_chart)
        mediator.register_on_item_remove_listener(self.draw_chart)
        
        self.draw_chart(None)

    def draw_chart(self, p):
        self.graph = Graph()
        self.graph.vp.pos = self.graph.new_vertex_property('vector<double>')
        self.graph.vp.name = self.graph.new_vertex_property('string')

        self.vertexes = []
        for player in Game.players:
            for phase in Game.phases:
                index = len(self.vertexes)
                self.vertexes.append(self.graph.add_vertex())
                self.graph.vp.pos[index] = [index, index]
                self.graph.vp.name[index] = player.name + "-" + phase.name[-1]
        self.vprops = { 'text' : self.graph.vp.name}

        if 'graph_widget' in vars(self):
            self.remove(self.graph_widget)

        self.graph_widget = GraphWidget(self.graph, self.graph.vp.pos, vprops = self.vprops)
        self.pack_start(self.graph_widget, True, True, 0)
        self.graph_widget.show()
