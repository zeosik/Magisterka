import logging


class Mediator:

    def __init__(self):
        self.player_types = MediatorTopic('player type')
        self.phases = MediatorTopic('phase')

        self.clear_state = MediatorOperation('clear state')

        #
        self.phase_select = MediatorOperation('phase select')
        self.rule_selects = MediatorOperation('rule select')
        self.model_select = MediatorOperation('model select')


class MediatorTopic:
    def __init__(self, name):
        self.name = name
        self.add = MediatorOperation('{0} - add'.format(name))
        self.select = MediatorOperation('{0} - select'.format(name))
        self.remove = MediatorOperation('{0} - remove'.format(name))


class MediatorOperation:

    def __init__(self, name):
        self.name = name
        self.log = logging.getLogger(self.__class__.__name__)
        self.listeners = []

    def register(self, listener):
        self.listeners.append(listener)

    def fire(self, sender, value):
        self.log.debug('firing operation: {0} val: {1}'.format(self.name, str(value)))
        for listener in self.listeners:
            listener(sender, value)
