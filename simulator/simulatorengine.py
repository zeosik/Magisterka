import logging

from common.model.gamemodel import GameModel
from common.model.rules.changephase import ChangePhase
from common.model.rules.wincheck import WinCheck
from common.model.rules.rule import Rule
from example import example_5_10_15
from common.model.phase import Phase
from common.model.player import Player
from common.model.playertype import PlayerType
from simulator.gamestate import simpleGameWithOnePlayerType, GameState

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

    def run(self):
        self.print_state()
        self.log.debug("Uruchamiam symulacje gry: " + self.gamestate.model.name)
        self.log.debug("Tura gracza: " + self.gamestate.current_player().name)
        self.log.debug("-Przechodze do fazy: " + self.gamestate.current_phase().name)

        while not self.gamestate.is_current_phase_end_game_phase():

            for rule in self.gamestate.current_phase().rules:
                self.log.debug("--Przetwarzam regule: " + rule.name)
                rule.apply(self.gamestate)

                if type(rule) is WinCheck:
                   self.gamestate.switch_phase(rule.phase)

        self.log.debug("Koncze symulacje")
        self.print_state()

def run():
    game = simpleGameWithOnePlayerType(example_5_10_15(), 3)
    engine = SimulatorEngine(game)
    engine.run()