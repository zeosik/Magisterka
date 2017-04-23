class Game:
    listeners = []
    players = []
    phases = []

    def add_player(player):
        Game.players.append(player)
        for listener in Game.listeners:
            listener()

    def add_phase(phase):
        Game.phases.append(phase)
        for listener in Game.listeners:
            listener()

    def register_on_game_changes(listener):
        Game.listeners.append(listener)
