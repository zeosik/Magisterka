import logging, itertools

from common.model.player import Player
from common.model.playerinput import PlayerInput
from common.model.rules.rule import Rule
from common.model.rules.rulepicker import RulePicker
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
            print (place + ": " + " ".join([artifact.name for artifact in places[place]]))

    def print_places_for_player(self, player: Player):
        self.print_places(self.get_places(player))

    def find_players(self):
        #tutaj serwer zgłasza jacy gracze będą grali w gre
        players = self.gamestate.players_for_type(self.gamestate.model.player_types[0])
        for player in players:
            player.isHuman = False
        #players[0].isHuman = True

    def run(self):
        self.print_places(self.get_places())
        self.log.debug("Uruchamiam symulacje gry: " + self.gamestate.model.name)
        self.log.debug("Tura gracza: " + self.gamestate.current_player().name)
        self.log.debug("-Przechodze do fazy: " + self.gamestate.current_phase().name)

        last_phase = None
        while not self.gamestate.is_current_phase_end_game_phase():

            if last_phase is not self.gamestate.current_phase():
                all_rules = self.gamestate.current_phase().rules
            else:
                all_rules = current_rule.next
            last_phase = self.gamestate.current_phase()

            rule_picker = RulePicker(all_rules)

            if self.gamestate.is_current_player_table_player():
                current_rule = self.table_turn(rule_picker)
            else:
                if self.gamestate.current_player().isHuman:
                    current_rule = self.player_turn(self.gamestate.current_player(), rule_picker)
                else:
                    current_rule = self.bot_turn(self.gamestate.current_player(), rule_picker)

            self.log.debug("--Przetwarzam regule: " + current_rule.name)
            current_rule.apply(self.gamestate)

        self.log.debug("Koncze symulacje")
        self.print_places(self.get_places())
        test_player = self.gamestate.type_players_dict[self.gamestate.model.player_types[0]][0]
        self.print_places(self.get_places(test_player))

    def table_turn(self, rule_picker: RulePicker) -> Rule:
        if rule_picker.requires_player_input(self.gamestate):
            self.log.error('table cannot pick a rule')
            raise Exception()

        rule = rule_picker.submitted()

        for player_input in rule.player_inputs():
            if player_input.requires_player_input(self.gamestate):
                self.log.error('table cannot make a choice')
                raise Exception()
        return rule

    def player_turn(self, player: Player, rule_picker: RulePicker) -> Rule:
        self.ask_human_for_choice(player, rule_picker)
        rule = rule_picker.submitted()
        for player_input in rule.player_inputs():
            if player_input.requires_player_input(self.gamestate):
                self.ask_human_for_choice(self.gamestate.current_player(), player_input)
        return rule

    def bot_turn(self, player: Player, rule_picker: RulePicker) -> Rule:
        for rule in self.bot_valid_combinations(rule_picker, self.gamestate):
            #TODO to i tak trzeba troche przemyslec ale jako tako dziala
            rule = rule[0]
            success = True
            made_choices = []
            for player_input in rule.player_inputs():
                if player_input.requires_player_input(self.gamestate):
                    all = self.bot_valid_combinations(player_input, self.gamestate)
                    if len(all) > 0:
                        bot_choice = all[-1]
                        player_input.submit_choices(bot_choice)
                        made_choices.append(bot_choice)
                    else:
                        success = False
            if success:
                self.log.debug('{0} choose rule: {1}'.format(player.name, rule.name))
                for choice in made_choices:
                    self.log.debug('made choice: {0}'.format([c.name for c in choice]))
                return rule

        self.log.error("No possible moves for player: " + player.name)
        raise Exception()

    def bot_valid_combinations(self, player_input: PlayerInput, gamestate: GameState) -> list:
        choices = player_input.all_choices(gamestate)
        all = []
        for length in range(len(choices) + 1):
            for subset in itertools.combinations(choices, length):
                if player_input.submit_choices(subset)[0]:
                    all.append(subset)
        return all



    # TODO osobna klasa z botem
    def ask_bot_for_choice(self, player: Player, player_input: PlayerInput):
        choices = player_input.all_choices(self.gamestate)
        all_cards_combinations = []

        for length in range(len(choices)+1):
            for subset in itertools.combinations(choices, length):
                if player_input.submit_choices(subset)[0]:
                    all_cards_combinations.append(subset)

        if len(all_cards_combinations) == 0:
            self.log.error("No possible moves for player: " + player.name)
            raise Exception()
        
        #TODO jak wybierać najlepsze rozwiąznie? Teraz wybieram to gdzie najwiecej kart
        chosen = all_cards_combinations[-1]
        player_input.submit_choices(chosen)
        self.log.debug(player.name + " zagral karty: " + " ".join([c.name for c in chosen]))

    def ask_human_for_choice(self, player: Player, player_input: PlayerInput):
        self.print_places_for_player(player)
        choices = player_input.all_choices(self.gamestate)
        print('{0} picks choice for: {1}'.format(player.name, player_input.name))
        for i, c in enumerate(choices):
            print('{0} - {1}'.format(i, c.name))
        while True:
            str = input('pick indexes: ')
            indexes = [int(s) for s_comma in str.split(',') for s in s_comma.split(' ') if len(s) > 0]

            #czy sa indeksy tylko z listy
            indexes_only_in_list = [j for j in indexes if 0 <= j < len(choices)]
            if len(indexes) != len(indexes_only_in_list):
                print('not valid indexes: {0}'.format([k for k in indexes if k not in indexes_only_in_list]))
                continue

            #czy nie ma duplikatów np [0,0]
            duplicated_indexes = [x for x in indexes_only_in_list if indexes_only_in_list.count(x) >= 2]
            if len(duplicated_indexes) != 0:
                print('duplicated indexes: {0}'.format(duplicated_indexes))
                continue

            #czy wybrane indeksy spelniaja warunki
            chosen = [choices[k] for k in indexes_only_in_list]
            success, msg = player_input.submit_choices(chosen)
            if not success:
                print(msg)
                continue

            return

def run():
    game = simpleGameWithOnePlayerType(example_5_10_15(), 3)
    engine = SimulatorEngine(game)
    engine.find_players()
    engine.run()