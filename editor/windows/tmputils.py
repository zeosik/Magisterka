from common.model.phase import Phase
from common.model.playerchooser.playerchooser import PlayerChooser
from common.model.rules.changephase import ChangePhase
from common.model.rules.foreachplayer import ForEachPlayer
from common.model.rules.ifrule import If
from common.model.rules.rule import Rule

tmp = {}

class TMPUTILS:
    def __init__(self):
        pass

    @staticmethod
    def player_color():
        return 'yellow'

    @staticmethod
    def table_color():
        return '#66CD00' #light green

    @staticmethod
    def start_rule_color():
        return 'cyan'

    @staticmethod
    def rule_color():
        return 'orange'

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
        for text, l in TMPUTILS.next_rules(rule).items():
            for r in l:
                if text not in all:
                    all[text] = []
                if r not in all[text]:
                    all[text].append(r)
                    TMPUTILS.append_rules(all, r)

    @staticmethod
    #TODO taki cheat
    def next_rules(rule) -> dict:
        if issubclass(rule.__class__, If):
            return { 'Yes': rule.if_true, 'No': rule.if_false }
        elif issubclass(rule.__class__, ForEachPlayer):
            if rule not in tmp:
                tmp[rule] = rule.create_actions(PlayerChooser('PlaceHolderPlayerChooser'))
            return { '': rule.next + tmp[rule] }
        else:
            return { '': rule.next }
