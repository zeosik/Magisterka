import logging

from common.model.gamemodel import GameModel
from common.model.phase import Phase
from common.model.places.place import Place
from common.model.player import Player
from common.model.playertype import PlayerType


class GameState:

    def __init__(self, model: GameModel, type_players_dict: dict):
        self.log = logging.getLogger(self.__class__.__name__)
        self.model = model
        #lista graczy dla każdego typu
        self.type_players_dict = type_players_dict
        #dla każdego typu trzymamy indeks aktualnego gracza
        self.type_current_player_dict = dict.fromkeys(type_players_dict, 0)
        #oznaczamy aktualny typ
        self.current_type = model.get_player_type_for_phase(model.start_phase)

        #aktualna faza dla każdego gracza
        self.player_current_phase = {}
        for players in self.type_players_dict.values():
            for player in players:
                self.player_current_phase[player] = None
        self.player_current_phase[self.current_player()] = model.start_phase

    def actual_place(self, player:Player, to_find_place: Place):
        matched = [place for place in player.places if place.name == to_find_place.name]
        if len(matched) == 1:
            return matched[0]
        else:
            self.log.error('too many places')
        self.log.error('could not find place: {0} for player: {1}'.format(to_find_place.name, player.name))
        raise Exception()

    def is_current_player_table_player(self):
        return self.current_player() == self.table_player()

    def players_for_type(self, type: PlayerType) -> list:
        return self.type_players_dict[type]

    def current_player_for_type(self, player_type: PlayerType) -> Player:
        return self.type_players_dict[player_type][self.current_player_index_for_type(player_type)]

    def current_player_index_for_type(self, player_type:PlayerType) -> int:
        return self.type_current_player_dict[player_type]

    def current_player_index(self) -> int:
        return self.current_player_index_for_type(self.current_type)

    def current_player(self) -> Player:
        return self.current_player_for_type(self.current_type)

    def current_phase_for_player(self, player: Player) -> Phase:
        return self.player_current_phase[player]

    def current_phase(self) -> Phase:
        return self.current_phase_for_player(self.current_player())

    def table_player(self) -> Player:
        return self.type_players_dict[self.model.table_type][0]

    def number_of_players(self):
        num = 0
        for player_type in self.model.player_types:
            num += len(self.players_for_type(player_type))
        return num

    def is_current_phase_end_game_phase(self) -> bool:
        return self.current_phase() == self.model.end_phase

    def switch_phase(self, phase: Phase):
        if phase not in self.current_type.phases:
            self.log.error('current player does not have phase. current type: {0} current player: {1} phase: {2}'.format(self.current_type.name, self.current_player().name, phase.name))
        self.player_current_phase[self.current_player()] = phase
        self.log.debug(" -Przechodze do fazy: " + phase.name)

    def switch_player(self, player: Player, phase: Phase):
        self.current_type = self.model.get_player_type_for_phase(phase)
        if player not in self.type_players_dict[self.current_type]:
            self.log.error("something went wrong")
        self.type_current_player_dict[self.current_type] = self.type_players_dict[self.current_type].index(player)
        self.log.debug(" Tura gracza: " + player.name)
        self.switch_phase(phase)


def simpleGameWithOnePlayerType(model: GameModel, numberOfPlayers: int) -> GameState:
    player_type = model.player_types[0]
    d = {
        player_type : [Player('player{0}'.format(i), player_type) for i in range(numberOfPlayers)],
        model.table_type : [Player('table-player', model.table_type)]
    }

    return GameState(model, d)