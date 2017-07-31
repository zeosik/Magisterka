import gi
import logging

from graph_tool import Graph
from graph_tool.draw import sfdp_layout, GraphWidget

from common.model.gamemodel import GameModel
from common.model.rules.move import Move
from common.model.rules.rule import Rule
from editor.mediator import Mediator
from editor.windows.tmputils import TMPUTILS

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class PlaceMapWindow(Gtk.ApplicationWindow):

    def __init__(self, app, mediator: Mediator):
        super().__init__(title='Place map', application=app)
        self.log = logging.getLogger(self.__class__.__name__)
        self.set_size_request(600, 400)
        self.move(700, 0)
        self.main_panel = Gtk.VBox()
        self.add(self.main_panel)

        self.mediator = mediator
        self.mediator.model_select.register(self.draw_for)
        self.mediator.phase_select.register(self.on_phase_select)
        self.mediator.rule_select.register(self.on_rule_select)

        self.rule_edge = None
        self.last_highlighted_edges = []
        self.graph = None
        self.place_vertex = None
        self.graph_widget = None

    def draw_for(self, sender, model: GameModel):
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
        graph.ep.color = graph.new_edge_property('vector<float>')

        for place in all_places:
            vertex = graph.add_vertex()
            place_vertex[place] = vertex

            graph.vp.name[vertex] = place.name
            graph.vp.color[vertex] = TMPUTILS.table_color() if place in model.table_type.places else TMPUTILS.player_color()
            graph.vp.text_pos[vertex] = 0

        self.graph = graph
        self.place_vertex = place_vertex

        self.rule_edge = {}
        for phase in model.all_phases():
            for source, target, rule in self.edge_info_for_phase(phase):
                    edge = graph.add_edge(place_vertex[source], place_vertex[target])
                    if rule not in self.rule_edge:
                        self.rule_edge[rule] = []
                    self.rule_edge[rule].append(edge)
                    graph.ep.color[edge] = [0.179, 0.203, 0.210, 0.8]

        pos = sfdp_layout(graph)

        vprops = {
            'text': graph.vp.name,
            'fill_color': graph.vp.color,
            'text_position': graph.vp.text_pos,
        }

        eprops = {
            'color': graph.ep.color
        }

        self.graph_widget = GraphWidget(graph, pos, vprops=vprops, eprops=eprops, vertex_size=50)
        self.main_panel.pack_start(self.graph_widget, True, True, 0)
        self.show_all()

    def on_phase_select(self, sender, phase):
        edges = []
        for source, target, rule in self.edge_info_for_phase(phase):
            edges += self.rule_edge[rule]

        self.highlight_edges(edges)

    def on_rule_select(self, sender, rule):
        self.highlight_edges(self.rule_edge[rule] if rule in self.rule_edge else [])

    def highlight_edges(self, edges):
        self.log.debug('highlighting edges')
        for edge in self.last_highlighted_edges:
            self.graph.ep.color[edge] = [0.179, 0.203, 0.210, 0.8]

        self.last_highlighted_edges = []
        for edge in edges:
            self.graph.ep.color[edge] = [0, 0, 255, 0.8]
            self.last_highlighted_edges.append(edge)

        # TODO nie wiem czemu ale to nie dziala,
        # TODO i trzeba przesunac jakis wierzcholek zeby zadzialalo odrysowanie na nowo -.-
        self.graph_widget.queue_draw()

    def edge_info_for_phase(self, phase):
        ret = []
        for rule in self.rules_for_phase(phase):
            if issubclass(rule.__class__, Move):
                source = rule.card_picker.source_place_picker.place
                target = rule.card_picker.target_place_picker.place
                ret.append((source, target, rule))
        return ret


    def rules_for_phase(self, phase):
        # TODO poprawilem w domu ajestem wpracy, pozniej zmienie
        start = Rule('start {0}'.format(phase.name))
        start.next = phase.rules
        rules = dict()
        rules[''] = [start]
        TMPUTILS.append_rules(rules, start)
        rules_set = set()
        for text, rule_list in rules.items():
            for rule in rule_list:
                rules_set.add(rule)
        return rules_set
