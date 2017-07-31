import logging

from common.model.phase import Phase
from common.model.playertype import PlayerType


class GameModel:

    def __init__(self, name):
        self.log = logging.getLogger(self.__class__.__name__)
        self.name = name
        self.player_types = []
        self.table_type = None

        self.starting_player = None
        self.start_phase = None
        self.end_phase = None

    def add_player_type(self, player_type: PlayerType) -> PlayerType:
        self.player_types.append(player_type)
        return player_type

    def add_table_type(self, table_type: PlayerType) -> PlayerType:
        self.table_type = table_type
        #?self.add_player_type(table_type)
        return table_type

    def get_player_type_for_phase(self, phase: Phase) -> PlayerType:
        for type in [self.table_type] + self.player_types:
            if phase in type.phases:
                return type
        self.log.error("couldn't find type for phase: {0}".format(phase.name))

    def all_player_types(self):
        return self.player_types + [self.table_type]

    def all_phases(self):
        return set([phase for type in self.all_player_types() for phase in type.phases])
