from common.model.playertype import PlayerType
from common.model.player import SelectPlayer, PlayerChooser
from common.model.rules.rule import Rule


class ForEachPlayer(Rule):
    def __init__(self, in_player_type: PlayerType, action: Rule):
        super().__init__('For each player in type {0} do {1}'.format(in_player_type.name, action.name))
        self.player_type = in_player_type
        self.action = action

    def apply(self, gamestate):
        #znajduje wszystkich graczy tego typu
        players_for_type = gamestate.type_players_dict[self.player_type]

        #dla self.action znajduje pole PlayerChooser o wartości EachPlayer
        #to pole bede podmieniać na kolejnych graczy
        for member in dir(self.action):
            obj = getattr(self.action, member)
            if type(obj) is PlayerChooser and obj.enum == SelectPlayer.EachPlayer:
                break
        
        #dla każdego gracza wywołuje self.action
        for index in range(len(players_for_type)):
            obj.enum = SelectPlayer.AtIndex
            obj.index = index
            self.action.apply(gamestate)