from simulator.network.client import Client

class HumanClient(Client):
    def __init__(self, name):
        super().__init__(name)

    def player_turn(self, gamestate, player, rule_picker):
        self.ask_human_for_choice(gamestate, player, rule_picker)
        rule = rule_picker.submitted()
        made_choices = dict()
        for player_input in rule.player_inputs():
            if player_input.requires_player_input(gamestate):
                choice = self.ask_human_for_choice(gamestate, player, player_input)
                index = rule.player_inputs().index(player_input)
                made_choices[index] = choice
        return rule_picker.all_rules.index(rule), made_choices

    def ask_human_for_choice(self, gamestate, player, player_input):
        choices = player_input.all_choices(gamestate)
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

            return chosen
