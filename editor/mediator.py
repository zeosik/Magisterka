
class Mediator:

    def __init__(self):
        self.add_player_listeners = []
        self.on_player_select_listeners = []
        self.add_phase_listeners = []
        self.on_phase_select_listeners = []

    # add player
    def add_player(self, player):
        for listener in self.add_player_listeners:
            listener(player)

    def register_on_player_add_listener(self, listener):
        self.add_player_listeners.append(listener)

    # select player
    def select_player(self, player):
        for listener in self.on_player_select_listeners:
            listener(player)

    def register_on_player_select_listener(self, listener):
        self.on_player_select_listeners.append(listener)

    # add phase
    def add_phase(self, phase):
        for listener in self.add_phase_listeners:
            listener(phase)

    def register_on_phase_add_listener(self, listener):
        self.add_phase_listeners.append(listener)

    # select phase
    def select_phase(self, phase):
        for listener in self.on_phase_select_listeners:
            listener(phase)

    def register_on_phase_select_listener(self, listener):
        self.on_phase_select_listeners.append(listener)