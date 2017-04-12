import gi
from graph_tool import Graph
from graph_tool.draw import GraphWidget

from editor.widgets.itemspanel.panelheader import PanelHeader

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class GeneralChartWidget(Gtk.VBox):

    def __init__(self):
        Gtk.VBox.__init__(self)

        self.header = PanelHeader('General view')

        self.pack_start(self.header, False, False, 0)

        self.graph = Graph()
        self.graph.vp.pos = self.graph.new_vertex_property('vector<double>')

        self.start = self.graph.add_vertex()
        self.graph.vp.pos[self.start] = [0, 0]
        self.end = self.graph.add_vertex()
        self.graph.vp.pos[self.end] = [1,1]

        self.graph_widget = GraphWidget(self.graph, self.graph.vp.pos)

        self.pack_start(self.graph_widget, True, True, 0)
