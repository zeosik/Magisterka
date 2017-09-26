import configparser

import logging

from common.model.phase import Phase
from common.model.rules.changephase import ChangePhase
from common.model.rules.rule import Rule

tmp = {}

class EditorConfig:
    def __init__(self, filename = 'display_properties.ini'):
        self.log = logging.getLogger(self.__class__.__name__)
        self.filename = filename
        self.config = configparser.ConfigParser()
        self.config.read(self.filename)

        self.colors = self.config['colors']

    def player_color(self, number = 1):
        return self.colors['player-type{0}'.format(number)]

    def table_color(self):
        return self.colors['table-type']

    def start_rule_color(self):
        return self.colors['start-rule']

    def rule_color(self, rule: Rule = None):
        ret = self.colors['rule']
        if rule is not None:
            name = 'rule-{0}'.format(rule.__class__.__name__)
            if name not in self.colors:
                self.log.warning("no default color for rule {0}".format(name))
            else:
                ret = self.colors[name]
        return ret

    def end_game_color(self):
        return self.colors['end-game']

    def start_game_color(self):
        return self.colors['start-game']

    def wrong_rule_color(self):
        return self.colors['wrong-rule']



class TMPUTILS:
    def __init__(self):
        pass

    @staticmethod
    def player_color():
        #return 'yellow'
        cfg = EditorConfig()
        return cfg.player_color()

    @staticmethod
    def table_color():
        #return '#66CD00' #light green
        cfg = EditorConfig()
        return cfg.table_color()

    @staticmethod
    def start_rule_color():
        #return 'cyan'
        cfg = EditorConfig()
        return cfg.start_rule_color()

    @staticmethod
    def end_game_color():
        cfg = EditorConfig()
        return cfg.end_game_color()

    @staticmethod
    def rule_color():
        #return 'orange'
        cfg = EditorConfig()
        return cfg.rule_color()

    @staticmethod
    def text_color(text: str):
        if text is 'Yes':
            return 'green'
        elif text is 'No':
            return 'red'
        return '#000000'

    @staticmethod
    def end_rule_color(rule, model):
        return TMPUTILS.table_color() if rule.phase in model.table_type.phases else TMPUTILS.player_color()


    @staticmethod
    def end_phases(phase: Phase):
        all_rules = dict()
        tmp = Rule('tmp')
        tmp.next = phase.rules
        TMPUTILS.append_rules(all_rules, tmp)
        return set([rule.phase for text, rule_list in all_rules.items() for rule in rule_list if issubclass(rule.__class__, ChangePhase)])

    @staticmethod
    def clear_container(container):
        for child in container.get_children():
            container.remove(child)

    @staticmethod
    def append_rules(all: dict, rule):
        for text, l in rule.rules_dict().items():
            for r in l:
                if text not in all:
                    all[text] = []
                if r not in all[text]:
                    all[text].append(r)
                    TMPUTILS.append_rules(all, r)
