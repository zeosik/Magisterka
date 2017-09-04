from analyzer.parameters.parameter import Parameter
import numpy

class CardUsageChecker(Parameter):
    def __init__(self):
        super().__init__("CardUsageChecker")
        self.usage_percentage = None
        
    def run(self, gamestate):
        used, unused = 0, 0
        for place in gamestate.table_player().places:
            for card in place.artifacts():
                if card.was_moved_at_least_once:
                    used += 1
                else:
                    unused += 1
        self.usage_percentage = used / (used + unused)

    def result(self):
        return self.usage_percentage

    def aggregate(self, analyzers):
        values = []
        for a in analyzers:
            values.append(a.parameters[self.name].result())
        return [(self.name + "[%]", int(numpy.average(values) * 100))]