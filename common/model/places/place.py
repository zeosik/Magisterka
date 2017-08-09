class Place:
    def __init__(self, name, starting_artifacts = None):
        self.name = name
        self._artifacts = starting_artifacts if starting_artifacts is not None else []
    
    def set_player(self, player):
        self.player = player

    def artifacts(self) -> list:
        return self._artifacts

    def remove_artifact(self, artifact):
        self._artifacts.remove(artifact)

    def add_artifact(self, artifact):
        self._artifacts.append(artifact)
