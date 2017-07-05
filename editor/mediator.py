

class Mediator:

    def __init__(self):
        self.player_types = MediatorTopic()
        self.phases = MediatorTopic()


class MediatorTopic:
    def __init__(self):
        self.add = MediatorOperation()
        self.select = MediatorOperation()
        self.remove = MediatorOperation()


class MediatorOperation:

    def __init__(self):
        self.listeners = []

    def register(self, listener):
        self.listeners.append(listener)

    def fire(self, sender, value):
        for listener in self.listeners:
            listener(sender, value)
