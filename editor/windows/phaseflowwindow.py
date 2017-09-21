from math import pi

import gi
import logging

from graph_tool import Graph, PropertyMap
from graph_tool.draw import GraphWidget, sfdp_layout

from common.model.gamemodel import GameModel
from common.model.phase import Phase
from common.model.rules.changephase import ChangePhase
from common.model.rules.ifrule import If
from common.model.rules.rule import Rule
from editor.mediator import Mediator
from editor.windows.tmputils import TMPUTILS

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class PhaseFlowWindow(Gtk.ApplicationWindow):
    def __init__(self, app, mediator: Mediator):
        super().__init__(title='Phase flow', application=app)
        self.log = logging.getLogger(self.__class__.__name__)
        self.set_size_request(600, 400)
        self.move(0, 0)
        self.main_panel = Gtk.VBox()
        self.add(self.main_panel)
        self.mediator = mediator
        self.mediator.phase_select.register(self.on_phase_select)
        self.mediator.model_select.register(self.on_model_select)
        self.model = None
        self.graph_widget = None

    def on_model_select(self, sender, model):
        self.model = model
        self.draw_for(model.start_phase, model)

    def on_phase_select(self, sender, phase):
        self.draw_for(phase, self.model)

    def draw_for(self, phase: Phase, model: GameModel):
        self.log.debug('drawing phase flow {0}'.format(phase.name))
        TMPUTILS.clear_container(self.main_panel)

        top = Gtk.HBox()

        name = Gtk.Label(phase.name)
        top.pack_start(name, True, True, 0)
        refresh_button = Gtk.Button('Refresh')
        refresh_button.connect('clicked', lambda w: self.draw_for(phase, model))
        top.pack_start(refresh_button, True, True, 0)
        self.main_panel.pack_start(top, False, False, 0)

        start = Rule('start {0}'.format(phase.name))
        start.next = phase.rules
        phase.rules = [start]

        rules_set = phase.all_rules_set()
        phase.rules = start.next

        graph = Graph()
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
        self.vertex_rule = {}

        for rule in rules_set:
            vertex = graph.add_vertex()
            rule_vertex[rule] = vertex
            self.vertex_rule[vertex] = rule
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
            for next_text, next_rule_list in rule.rules_dict().items():
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
        self.graph_widget = GraphWidget(graph, pos, display_props=[graph.vp.fullname], vprops=vprops, eprops=eprops,
                                   vertex_size=50)
        #jest cos takiego jak GraphWidget.key_press_callback ale u mnie nie dziala...
        self.graph_widget.connect('button-release-event', self.on_vertex_clicked)

        self.main_panel.pack_start(self.graph_widget, True, True, 0)
        self.show_all()

    def on_vertex_clicked(self, widget, event):
        if widget.picked is not None:
            if type(widget.picked) == PropertyMap:
                rules = [self.vertex_rule[v] for v in self.vertex_rule.keys() if widget.picked[v]]
            else:
                rules = [self.vertex_rule[widget.picked]]
            self.mediator.rule_selects.fire(self, rules)
