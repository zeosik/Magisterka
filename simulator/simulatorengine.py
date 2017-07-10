import logging

from common.model.gamemodel import GameModel
from common.model.rules.changephase import ChangePhase
from common.model.rules.wincheck import WinCheck
from common.model.rules.rule import Rule
from example import example_5_10_15
from common.model.phase import Phase
from common.model.player import Player, SelectPlayer
from common.model.playertype import PlayerType

#tymczasowe generowanie graczy
from simulator.gamestate import simpleGameWithOnePlayerType, GameState


def get_players_for_types(player_types, num_each_type, table_type):
    players_for_types = dict()
    for player_type in player_types:
        players = []
        for i in range(num_each_type):
            players.append(Player('player' + str(i), player_type))
        players_for_types[player_type] = players
    players_for_types[table_type] = Player('table', table_type)
    return players_for_types

class SimulatorEngine():
    def __init__(self, gamestate: GameState):
        self.log = logging.getLogger(self.__class__.__name__)
        self.gamestate = gamestate

    def print_state(self):
        self.log.debug("Stan gry:")

        for place in self.gamestate.table_player().places:
            self.log.debug("-" + place.name + ": " + " ".join(map(str, place.artifacts)))

        for player_type in self.gamestate.model.player_types:
            for player in self.gamestate.type_players_dict[player_type]:
                for place in player.places:
                    self.log.debug("-" + player.name + ":" + place.name + ": " + " ".join(map(str, place.artifacts)))

    #def swich_phase(self, phase):
    #    self.current_phase = phase
    #    self.log.debug("-Przechodze do fazy: " + self.current_phase.name)

    #def swich_player(self, player):
#        if player == self.gamestate.type_players_dict[self.gamestate.model.table_type]:
#            self.is_table_turn = True
#        else:
#            self.is_table_turn = False
#            self.current_player = player
#        self.log.debug("Tura gracza: " + player.name)

    def run(self):
        self.print_state()
        self.log.debug("Uruchamiam symulacje gry: " + self.gamestate.model.name)
        self.log.debug("Tura gracza: " + self.gamestate.current_player().name)
        self.log.debug("-Przechodze do fazy: " + self.gamestate.current_phase().name)

        while not self.gamestate.is_current_phase_end_game_phase():

            for rule in self.gamestate.current_phase().rules:
                self.log.debug("--Przetwarzam regule: " + rule.name)
                rule.apply()

                if type(rule) is ChangePhase:
                    #self.gamestate.switch_phase(rule.phase)

                    if (rule.player == SelectPlayer.FirstPlayer):
                        self.gamestate.switch_player(self.gamestate.type_players_dict[self.gamestate.model.player_types[0]][0], rule.phase)

                    elif (rule.player == SelectPlayer.NextPlayer):
                        #TODO narazie takie obejscie
                        p_type = self.gamestate.model.player_types[0]
                        p_index = self.gamestate.current_player_index_for_type(p_type)
                        num_players = len(self.gamestate.type_players_dict[p_type])
                        self.gamestate.switch_player(self.gamestate.type_players_dict[p_type][(p_index+1) % num_players], rule.phase)

                    elif (rule.player == SelectPlayer.TablePlayer):
                        self.gamestate.switch_player(self.gamestate.table_player(), rule.phase)

                elif type(rule) is WinCheck:
                   self.gamestate.switch_phase(rule.phase)

        self.log.debug("Koncze symulacje")
        self.print_state()

def run():
    game = simpleGameWithOnePlayerType(example_5_10_15(), 3)
    engine = SimulatorEngine(game)
    engine.run()