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
    def __init__(self, game: GameModel):
        self.log = logging.getLogger(self.__class__.__name__)
        self.game = game
        self.current_phase = self.game.start_phase

        #self.players to jest słownik z tablicami graczy
        #czyli mamy np self.players['players'] i tam są gracze 'player0' i 'player1'
        #dla self.players['table-player'] nie ma tablicy, tylko pojedynczy gracz 'table'
        #Nie wiem jak to lepiej przechowywać, jak masz jakiś pomysł to śmiało
        self.players = get_players_for_types(self.game.player_types, 2, self.game.table_type)

        # stół nie może być graczem, bo przy wartości "NextPlayer" się zgubimy (nie wiemy kto grał wcześniej)
        self.current_player = None
        self.is_table_turn = True

    def print_state(self):
        self.log.debug("Stan gry:")

        for place in self.players[self.game.table_type].places:
            self.log.debug("-" + place.name + ": " + " ".join(map(str, place.artifacts)))

        for player_type in self.game.player_types:
            for player in self.players[player_type]:
                for place in player.places:
                    self.log.debug("-" + player.name + ":" + place.name + ": " + " ".join(map(str, place.artifacts)))

    def swich_phase(self, phase):
        self.current_phase = phase
        self.log.debug("-Przechodze do fazy: " + self.current_phase.name)

    def swich_player(self, player):
        if player == self.players[self.game.table_type]:
            self.is_table_turn = True
        else:
            self.is_table_turn = False
            self.current_player = player
        self.log.debug("Tura gracza: " + player.name)

    def run(self):
        self.print_state()
        self.log.debug("Uruchamiam symulacje gry: " + self.game.name)
        self.log.debug("Tura gracza: " + self.players[self.game.table_type].name)
        self.log.debug("-Przechodze do fazy: " + self.current_phase.name)

        while self.current_phase != self.game.end_phase:

            for rule in self.current_phase.rules:
                self.log.debug("--Przetwarzam regule: " + rule.name)
                rule.apply()

                if type(rule) is ChangePhase:
                    self.swich_phase(rule.phase)

                    if (rule.player == SelectPlayer.FirstPlayer):
                        self.swich_player(self.players[self.game.player_types[0]][0])

                    elif (rule.player == SelectPlayer.NextPlayer):                        
                        p_type = self.current_player.type
                        p_index = self.players[p_type].index(self.current_player)
                        num_players = len(self.players[p_type])
                        self.swich_player(self.players[p_type][(p_index+1) % num_players])

                    elif (rule.player == SelectPlayer.TablePlayer):
                        self.swich_player(self.players[self.game.table_type])

                elif type(rule) is WinCheck:
                   self.swich_phase(rule.phase)

        self.log.debug("Koncze symulacje")
        self.print_state()

def run():
    engine = SimulatorEngine(example_5_10_15())
    engine.run()