class Place:
    def __init__(self, name, starting_artifacts = []):
        self.name = name
        self.artifacts = starting_artifacts
    
    def set_player(self, player):
        self.player = player