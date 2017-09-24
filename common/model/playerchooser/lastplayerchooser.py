from common.model.playerchooser.constantplayerchooser import ConstantPlayerChooser
from common.model.playerchooser.playerchooser import PlayerChooser
from common.model.playertype import PlayerType
from simulator.gamestate import GameState


class LastPlayerChooser(PlayerChooser):

    def __init__(self, player_type: PlayerType, condition = None):
        super().__init__('Last Player Chooser')
        self.player_type = player_type
        self.condition = condition

    def auto_submitted_values(self, gamestate: GameState):
        all_players = gamestate.players_for_type(self.player_type)
        for i in range(len(all_players)):
            player_candidate = all_players[-1 -i]
            if self.condition is not None and not self.condition(gamestate, player_candidate):
                return [player_candidate]
        raise Exception('no candidate for last player')
        #return [gamestate.players_for_type(self.player_type)[-1]]