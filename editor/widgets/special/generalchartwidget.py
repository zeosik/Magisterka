import gi
from graph_tool import Graph
from graph_tool.draw import GraphWidget

from editor.widgets.itemspanel.panelheader import PanelHeader

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class GeneralChartWidget(Gtk.VBox):

    def __init__(self, mediator):
        Gtk.VBox.__init__(self)

        self.players = []
        self.phases = []

        self.header = PanelHeader('General view')

        self.pack_start(self.header, False, False, 0)

        mediator.players.register_add(self.on_player_add)
        mediator.phases.register_add(self.on_phase_add)
        mediator.players.register_remove(self.on_player_remove)
        mediator.phases.register_remove(self.on_phase_remove)

        self.draw_chart()

    def on_player_add(self, player):
        self.players.append(player)
        self.draw_chart()

    def on_phase_add(self, phase):
        self.phases.append(phase)
        self.draw_chart()

    def on_player_remove(self, player):
        self.players.remove(player)
        self.draw_chart()

    def on_phase_remove(self, phase):
        self.phases.remove(phase)
        self.draw_chart()

    def draw_chart(self):
        self.graph = Graph()
        self.graph.vp.pos = self.graph.new_vertex_property('vector<double>')
        self.graph.vp.name = self.graph.new_vertex_property('string')

        self.vertexes = []
        for player in self.players:
            for phase in self.phases:
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
