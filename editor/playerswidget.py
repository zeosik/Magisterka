import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from graph_tool.all import *
from graph_tool.draw import GraphWidget

from editor.player import *


class PlayersWidget(Gtk.Box):

    def __init__(self):
        Gtk.Box.__init__(self)

        self.players_graph = Graph()
        self.players_graph.vp.players = self.players_graph.new_vertex_property('object')
        self.players_graph.vp.text = self.players_graph.new_vertex_property('string')
        self.players_graph.vp.pos = self.players_graph.new_vertex_property('vector<double>')

        vprops = {'text' : self.players_graph.vp.text}
        self.players_widget = GraphWidget(self.players_graph, self.players_graph.vp.pos, vprops=vprops)

        self.pack_start(self.players_widget, True, True, 0)

    def add_player(self, player):
        player_vertex = self.players_graph.add_vertex()
        self.players_graph.vp.players[player_vertex] = player
        self.players_graph.vp.text[player_vertex] = player.name
        self.players_graph.vp.pos[player_vertex] = [self.players_graph.num_vertices(), self.players_graph.num_vertices()]
