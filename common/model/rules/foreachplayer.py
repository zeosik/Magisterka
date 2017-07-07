from common.model.playertype import PlayerType
from common.model.rules.rule import Rule


class ForEachPlayer(Rule):
    def __init__(self, in_player_type: PlayerType, action: Rule):
        super().__init__('For each player in type {0} do {1}'.format(in_player_type.name, action.name))
        self.player_type = in_player_type
        self.action = action
