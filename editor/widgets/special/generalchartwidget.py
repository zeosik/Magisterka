import gi
from graph_tool import Graph
from graph_tool.draw import GraphWidget

from editor.widgets.itemspanel.panelheader import PanelHeader
from common.player import Player
from common.phase import Phase

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class GeneralChartWidget(Gtk.VBox):

    def __init__(self):
        Gtk.VBox.__init__(self)

        self.header = PanelHeader('General view')

        self.pack_start(self.header, False, False, 0)

        self.graph = Graph()
        self.graph.vp.pos = self.graph.new_vertex_property('vector<double>')
        self.graph.vp.name = self.graph.new_vertex_property('string')

        #TODO Update those tables from left panel
        self.players = [Player("Alice"), Player("Bob")]
        self.phases = [Phase("1"), Phase("2")]

        self.vertexes = []
        for player in self.players:
            for phase in self.phases:
                index = len(self.vertexes)
                self.vertexes.append(self.graph.add_vertex())
                self.graph.vp.pos[index] = [index, index]
                self.graph.vp.name[index] = player.name + "-" + phase.name
        vprops = {'text' : self.graph.vp.name}

        self.graph_widget = GraphWidget(self.graph, self.graph.vp.pos, vprops = vprops)

        self.pack_start(self.graph_widget, True, True, 0)
