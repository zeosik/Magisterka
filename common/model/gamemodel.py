from common.model.playertype import PlayerType


class GameModel:

    def __init__(self, name):
        self.name = name
        self.player_types = []
        self.table_type = None

        self.starting_player = None
        self.start_phase = None
        self.end_phase = None

    def add_player_type(self, player_type: PlayerType):
        self.player_types.append(player_type)
        return player_type

    def add_table_type(self, table_type: PlayerType):
        self.table_type = table_type
        #?self.add_player_type(table_type)
        return table_type
