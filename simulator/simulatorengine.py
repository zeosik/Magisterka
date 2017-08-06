import logging, itertools, threading

from common.model.player import Player
from common.model.playerinput import PlayerInput
from common.model.rules.rule import Rule
from common.model.rules.rulepicker import RulePicker
from simulator.network.server import Server
from simulator.network.botclient import BotClient
from simulator.network.humanclient import HumanClient
from example import example_5_10_15, example_card_sequence
from simulator.gamestate import simpleGameWithOnePlayerType, GameState
from analyzer.singlegameanalyzer import SingleGameAnalyzer


class SimulatorEngine():
    def __init__(self, gamestate: GameState, num_humans, analyze_game):
        self.log = logging.getLogger(self.__class__.__name__)
        self.gamestate = gamestate
        self.num_humans = num_humans
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
        if not self.analyze_game:
            for place in sorted(places):
                print (place + ": " + " ".join([artifact.name for artifact in places[place]]))

    def print_places_for_player(self, player: Player):
        self.print_places(self.get_places(player))

    def prepare_server_and_clients(self):
        for index in range(self.gamestate.number_of_players()):
            if index < self.num_humans:
                client = HumanClient("player" + str(index))
            else:
                client = BotClient("player" + str(index))
            client_thread = threading.Thread(target=client.run)
            client_thread.start()
        self.server.accept_clients()

    def run(self):
        self.log.debug("Uruchamiam symulacje gry: " + self.gamestate.model.name)
        self.log.debug("Tura gracza: " + self.gamestate.current_player().name)
        self.log.debug("-Przechodze do fazy: " + self.gamestate.current_phase().name)

        last_phase = None
        while not self.gamestate.is_current_phase_end_game_phase():

            if self.analyze_game:
                self.analyzer.run_analysis(self.gamestate)

            if last_phase is not self.gamestate.current_phase():
                all_rules = self.gamestate.current_phase().rules
            else:
                all_rules = current_rule.next
            last_phase = self.gamestate.current_phase()

            rule_picker = RulePicker(all_rules)

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
            current_rule.apply(self.gamestate)

        self.server.close_connections()
        self.log.debug("Koncze symulacje")
        self.print_places(self.get_places())
        
        if self.analyze_game:
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

def run(game_name, num_players, num_humans, analyze_game = False):
    if game_name=="5_10_15":
        game = simpleGameWithOnePlayerType(example_5_10_15(), num_players)
    elif game_name=="5_10_15_one_phase":
        game = simpleGameWithOnePlayerType(example_5_10_15(False), num_players)
    else: #game_name=="card_sequence":
        game = simpleGameWithOnePlayerType(example_card_sequence(), num_players)
    
    engine = SimulatorEngine(game, num_humans, analyze_game)
    engine.prepare_server_and_clients()
    return engine.run()