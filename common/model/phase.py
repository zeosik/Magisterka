
class Phase:

    def __init__(self, name):
        self.name = name
        self.rules = []

    def append_rule(self, rule): #Rule
        self.rules.append(rule)
