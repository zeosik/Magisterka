import logging, itertools, threading

from common.model.player import Player
from common.model.playerinput import PlayerInput
from common.model.rules.changephase import ChangePhase
from common.model.rules.rule import Rule
from common.model.rules.rulepicker import RulePicker
from simulator.network.server import Server
from simulator.network.botclient import BotClient
from simulator.network.humanclient import HumanClient
from example import *
from simulator.gamestate import simpleGameWithOnePlayerType, GameState
from analyzer.singlegameanalyzer import SingleGameAnalyzer


class SimulatorEngine():
    def __init__(self, gamestate: GameState, num_humans, num_random_bots, analyze_game):
        self.log = logging.getLogger(self.__class__.__name__)
        self.gamestate = gamestate
        self.num_humans = num_humans
        self.num_random_bots = num_random_bots
        self.analyze_game = analyze_game
        self.server = Server(self.gamestate.number_of_players())
        if self.analyze_game:
            self.analyzer = SingleGameAnalyzer()

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
            self.log.info(place + ": " + " ".join([artifact.name for artifact in places[place]]))

    def print_places_for_player(self, player: Player):
        self.print_places(self.get_places(player))

    def prepare_server_and_clients(self):
        for index in range(self.gamestate.number_of_players()):
            if index < self.num_humans:
                client = HumanClient("player" + str(index))
            else:
                if index < self.num_humans + self.num_random_bots:
                    client = BotClient("player" + str(index), True)
                else:
                    client = BotClient("player" + str(index), False)
            client_thread = threading.Thread(target=client.run)
            client_thread.start()
        self.server.accept_clients()

    def run(self):
        self.log.debug("Uruchamiam symulacje gry: " + self.gamestate.model.name)
        self.log.debug("Tura gracza: " + self.gamestate.current_player().name)
        self.log.debug("-Przechodze do fazy: " + self.gamestate.current_phase().name)

        last_phase = None
        last_rule_was_change_phase = True
        while not self.gamestate.is_current_phase_end_game_phase():

            if last_rule_was_change_phase:
            #if last_phase is None or issubclass(last_phase.__class__, ChangePhase):
            #if last_phase is not self.gamestate.current_phase():
                all_rules = self.gamestate.current_phase().rules
            else:
                all_rules = current_rule.next
            last_phase = self.gamestate.current_phase()

            rule_picker = RulePicker(all_rules)

            if self.analyze_game:
                self.analyzer.run_analysis(self.gamestate, rule_picker)

            if self.gamestate.is_current_player_table_player():
                current_rule = self.table_turn(rule_picker)
            else:
                self.print_places_for_player(self.gamestate.current_player())
                data_for_client = (self.gamestate, self.gamestate.current_player(), rule_picker)
                answer = self.server.ask_for_choice(data_for_client, self.gamestate.current_player().name)
                current_rule = rule_picker.all_rules[answer[0]] #rule wybrana przez gracza
                player_inputs = current_rule.player_inputs()

                for player_input in player_inputs:
                    player_input.requires_player_input(self.gamestate) # musimy to zawołać bo to ustawia domyślne wartości

                for index, choice in answer[1].items():     # Ustalamy które obiekty zostały wybrane (dostaliśmy inne (skopiowane) obiekty)
                    real_choice = []
                    all_artifacts = [j for i in self.get_places().values() for j in i] #wszystkie artefakty które są w grze
                    for artifact in choice:
                        for artifact_real in all_artifacts:
                            if artifact.__dict__ == artifact_real.__dict__:
                                real_choice.append(artifact_real)
                    player_inputs[index].submit_choices(real_choice)
            self.log.debug('apply {0}'.format(current_rule.name))
            self.print_places(self.get_places())
            current_rule.apply(self.gamestate)
            last_rule_was_change_phase = issubclass(current_rule.__class__, ChangePhase)

        self.server.close_connections()
        self.log.debug("Koncze symulacje")
        self.print_places(self.get_places())
        self.log.info("Wygral " + self.gamestate.current_player_for_type(self.gamestate.model.player_types[0]).name)
                
        if self.analyze_game:
            self.analyzer.run_end_game_analysis(self.gamestate)
            return self.analyzer

    def table_turn(self, rule_picker: RulePicker) -> Rule:
        if rule_picker.requires_player_input(self.gamestate):
            self.log.error('table cannot pick a rule')
            raise Exception()

        rule = rule_picker.submitted()

        for player_input in rule.player_inputs():
            if player_input.requires_player_input(self.gamestate):
                self.log.error('table cannot make a choice for rule: {0}'.format(rule.name))
                raise Exception()
        return rule

def run(game_name, num_players, num_humans, num_random_bots = 0, analyze_game = False):
    games = dict()
    config_file = open("games_list.txt", "r")
    for line in config_file.readlines():
        games[line.split()[0]] = line.split()[1]
    config_file.close()

    try:
        game = simpleGameWithOnePlayerType(eval(games[game_name]), num_players)
    except:
        raise Exception("game name not implemented or not listed in games_list.txt")
    
    engine = SimulatorEngine(game, num_humans, num_random_bots, analyze_game)
    engine.prepare_server_and_clients()
    return engine.run()