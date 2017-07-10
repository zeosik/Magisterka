from common.model.rules.rule import Rule
from common.model.player import Player, SelectPlayer, PlayerChooser
from common.model.places.place import Place

class CardOperationRule(Rule):

    def __init__(self, name):
        super().__init__(name)

    def find_player(self, gamestate, player: PlayerChooser) -> Player:
        if player.enum == SelectPlayer.TablePlayer:
            return gamestate.table_player()

        if player.enum == SelectPlayer.AtIndex:
            return gamestate.type_players_dict[player.type][player.index]

        if player.enum == SelectPlayer.FirstPlayer:
            return gamestate.type_players_dict[player.type][0]
        #TODO reszta wartosci?

    def find_place(self, player: Player, placename) -> Place:
        for place in player.places:
            if placename == place.name:
                return place