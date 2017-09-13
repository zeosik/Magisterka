import itertools
from random import randint

from simulator.network.client import Client

class BotClient(Client):
    def __init__(self, name, random_bot = False):
        super().__init__(name)
        self.random_bot = random_bot

    def player_turn(self, gamestate, player, rule_picker):
        for rule in self.bot_valid_combinations(rule_picker, gamestate):
            #TODO to i tak trzeba troche przemyslec ale jako tako dziala
            rule = rule[0]
            success = True
            made_choices = dict()
            for player_input in rule.player_inputs():
                if player_input.requires_player_input(gamestate):
                    all = self.bot_valid_combinations(player_input, gamestate)
                    if len(all) > 0:
                        if self.random_bot:
                            bot_choice = all[randint(0, len(all) - 1)]
                        else:
                            bot_choice = all[-1]
                        index = rule.player_inputs().index(player_input)
                        made_choices[index] = bot_choice
                    else:
                        success = False
            if success:
                self.log.debug('{0} choose rule: {1}'.format(player.name, rule.name))
                for name, choice in made_choices.items():
                    self.log.debug('made choice: {0}'.format([c.name for c in choice]))
                return rule_picker.all_rules.index(rule), made_choices

        self.log.error("No possible moves for player: " + player.name)
        raise Exception()

    def bot_valid_combinations(self, player_input, gamestate) -> list:
        choices = player_input.all_choices(gamestate)
        all = []
        for length in range(len(choices) + 1):
            for subset in itertools.combinations(choices, length):
                if player_input.submit_choices(subset)[0]:
                    all.append(subset)
        return all