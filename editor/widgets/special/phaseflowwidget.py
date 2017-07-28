from math import pi

import gi
import logging

from graph_tool import Graph
from graph_tool.draw import GraphWidget, sfdp_layout

from common.model.gamemodel import GameModel
from common.model.phase import Phase
from common.model.rules.changephase import ChangePhase
from common.model.rules.ifrule import If
from common.model.rules.rule import Rule
from editor.windows.tmputils import TMPUTILS

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class PhaseFlowWidget(Gtk.VBox):
    def __init__(self):
        super().__init__()
        self.log = logging.getLogger(self.__class__.__name__)

        self.add(Gtk.Label(self.__class__.__name__))

    def draw_for(self, phase: Phase, model: GameModel):
        self.log.debug('drawing phase flow {0}'.format(phase.name))
        for child in self.get_children():
            self.remove(child)

        name = Gtk.Label(phase.name)
        self.pack_start(name, False, False, 0)

        start = Rule('start {0}'.format(phase.name))
        start.next = phase.rules
        # phase.rules = [start]

        rules = dict()
        rules[''] = [start]
        TMPUTILS.append_rules(rules, start)

        rules_set = set()
        for text, rule_list in rules.items():
            for rule in rule_list:
                rules_set.add(rule)

        # for rule in rules:
        #    label = Gtk.Label(rule.name[:30])
        #    self.phase_panel.pack_start(label, True, True, 0)

        graph = Graph()
        # graph.vp.pos = graph.new_vertex_property('vector<double>')
        graph.vp.name = graph.new_vertex_property('string')
        graph.vp.fullname = graph.new_vertex_property('string')
        graph.vp.color = graph.new_vertex_property('string')
        graph.vp.shape = graph.new_vertex_property('string')
        graph.vp.rotation = graph.new_vertex_property('float')
        graph.vp.text_pos = graph.new_vertex_property('float')
        graph.vp.text_rotation = graph.new_vertex_property('float')

        graph.ep.text = graph.new_edge_property('string')
        graph.ep.text_color = graph.new_edge_property('string')

        rule_vertex = {}
        self.vertex_full_name = {}

        for rule in rules_set:
            vertex = graph.add_vertex()
            rule_vertex[rule] = vertex
            self.vertex_full_name[vertex] = rule.name
            graph.vp.name[vertex] = rule.simple_name()
            graph.vp.fullname[vertex] = rule.name
            if rule is start:
                color = TMPUTILS.start_rule_color()
            elif issubclass(rule.__class__, ChangePhase):
                color = TMPUTILS.end_rule_color(rule, model)
            else:
                color = TMPUTILS.rule_color()
            graph.vp.color[vertex] = color
            graph.vp.shape[vertex] = 'square' if issubclass(rule.__class__, If) else 'circle'
            graph.vp.rotation[vertex] = pi / 4 if issubclass(rule.__class__, If) else 0
            graph.vp.text_pos[vertex] = 0
            graph.vp.text_rotation[vertex] = - pi / 4 if issubclass(rule.__class__, If) else 0

        for rule in rules_set:
            for next_text, next_rule_list in TMPUTILS.next_rules(rule).items():
                for next_rule in next_rule_list:
                    edge = graph.add_edge(rule_vertex[rule], rule_vertex[next_rule])
                    graph.ep.text[edge] = next_text
                    graph.ep.text_color[edge] = TMPUTILS.text_color(next_text)

        pos = sfdp_layout(graph)

        vprops = {
            'text': graph.vp.name,
            'fill_color': graph.vp.color,
            'shape': graph.vp.shape,
            'rotation': graph.vp.rotation,
            'text_position': graph.vp.text_pos,
            'text_rotation': graph.vp.text_rotation
        }
        eprops = {
            'text': graph.ep.text,
            'text_color': graph.ep.text_color
        }
        graph_widget = GraphWidget(graph, pos, display_props=[graph.vp.fullname], vprops=vprops, eprops=eprops,
                                   vertex_size=50)
        #graph_widget.connect('button-release-event', self.on_vertex_clicked)

        self.pack_start(graph_widget, True, True, 0)
        self.show_all()
