import logging

from example import example_5_10_15
from simulator.gamestate import simpleGameWithOnePlayerType, GameState

class SimulatorEngine():
    def __init__(self, gamestate: GameState):
        self.log = logging.getLogger(self.__class__.__name__)
        self.gamestate = gamestate

    def get_places(self, player_arg = None):
        all_places = dict()
        for place in self.gamestate.table_player().places:
            name = self.gamestate.table_player().name + ":" + place.name
            all_places[name] = place.get_cards(player_arg)

        for player_type in self.gamestate.model.player_types:
            for player in self.gamestate.type_players_dict[player_type]:
                for place in player.places:
                    all_places[player.name + ":" + place.name] = place.get_cards(player_arg)
        return all_places

    def print_places(self, places):
        for place in sorted(places):
            print (place + ": " + " ".join(map(str, places[place])))

    def run(self):
        self.print_places(self.get_places())
        self.log.debug("Uruchamiam symulacje gry: " + self.gamestate.model.name)
        self.log.debug("Tura gracza: " + self.gamestate.current_player().name)
        self.log.debug("-Przechodze do fazy: " + self.gamestate.current_phase().name)

        while not self.gamestate.is_current_phase_end_game_phase():

            for rule in self.gamestate.current_phase().rules:
                self.log.debug("--Przetwarzam regule: " + rule.name)
                rule.apply(self.gamestate)

        self.log.debug("Koncze symulacje")
        self.print_places(self.get_places())
        test_player = self.gamestate.type_players_dict[self.gamestate.model.player_types[0]][0]
        self.print_places(self.get_places(test_player))

def run():
    game = simpleGameWithOnePlayerType(example_5_10_15(), 3)
    engine = SimulatorEngine(game)
    engine.run()