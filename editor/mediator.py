

class Mediator:

    def __init__(self):
        self.players = MediatorTopic()
        self.phases = MediatorTopic()


class MediatorTopic:
    def __init__(self):
        self.add_listeners = []
        self.select_listeners = []
        self.remove_listeners = []

    def add(self, value):
        for listener in self.add_listeners:
            listener(value)

    def register_add(self, listener):
        self.add_listeners.append(listener)

    def select(self, value):
        for listener in self.select_listeners:
            listener(value)

    def register_select(self, listener):
        self.select_listeners.append(listener)

    def remove(self, value):
        for listener in self.remove_listeners:
            listener(value)

    def register_remove(self, listener):
        self.remove_listeners.append(listener)
