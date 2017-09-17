

class Phase:

    def __init__(self, name):
        self.name = name
        self.rules = []

    def append_rule(self, rule): #Rule
        self.rules.append(rule)

    def all_rules_set(self) -> set:
        from common.model.rules.changephase import ChangePhase

        ret = set()
        to_visit = self.rules
        while to_visit:
            rule = to_visit[0]
            to_visit = to_visit[1:]

            ret.add(rule)

            if not issubclass(rule.__class__, ChangePhase):
                for text, rules in rule.rules_dict().items():
                    to_visit += [rule for rule in rules if rule not in ret]

        return ret
