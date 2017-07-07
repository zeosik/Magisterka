from common.articaft_generators.cardgenerator import CardGenerator
from common.model.artifacts.card import CardColor
from common.model.gamemodel import GameModel
from common.model.phase import Phase
from common.model.places.place import Place
from common.model.playertype import PlayerType
from common.model.player import Player, SelectPlayer
from common.model.rules.changephase import ChangePhase
from common.model.rules.wincheck import WinCheck
from common.model.rules.foreachplayer import ForEachPlayer
from common.model.rules.move import Move
from common.model.rules.shuffle import Shuffle

def current_player_for_type(player_type):
    pass

#class FOO:
#    def __init__(self, name):
#        self.name = name

def example_5_10_15():

    game = GameModel('5-10-15')

    #
    table_type = game.add_table_type(PlayerType('table-type'))
    player_type = game.add_player_type(PlayerType('players'))
    player_type.min_players = 2
    player_type.max_players = 10

    #?
    TABLE_PLAYER = SelectPlayer.TablePlayer #FOO('table-player')
    player = SelectPlayer.EachPlayer #FOO('player')

    # rekwizyty
    cards = CardGenerator.cards(min_rank=1, max_rank=10, colors=list(CardColor))

    #miejsca
    player_hand = player_type.add_place(Place('hand'))
    deck = table_type.add_place(Place('deck', starting_artifacts=cards))
    discard_pile = table_type.add_place(Place('discard pile'))

    #fazy
    phase_start = table_type.add_phase(Phase('start'))
    game.start_phase = phase_start
    phase_end = table_type.add_phase(Phase('end'))
    game.end_phase = phase_end
    phase_choose_player = table_type.add_phase(Phase('choose-player'))
    phase_win_check = table_type.add_phase(Phase('win-check'))
    phase1 = player_type.add_phase(Phase('phase1'))

    #faza - rozdanie poczatkowe
    #list<Player>, int -> int
    #Może jakas klasa? PlayerChoose?
    #firstPlayer = lambda players_list, current_index: 1
    firstPlayer = SelectPlayer.FirstPlayer #FOO('first-player')
    #nextPlayer = lambda players_list, current_index: (current_index + 1) % len(players_list)
    nextPlayer = SelectPlayer.NextPlayer #FOO('next_player')

    phase_start.rules.append(Shuffle(TABLE_PLAYER, deck))
    #Move(from_player_type, from_player_in_this_type, from_pile_in_this_player, to_player_type, to_player, to_pile)
    #Player -> Rule
    give_5_cards = Move(TABLE_PLAYER, deck, player, player_hand, number_of_cards=5)
    phase_start.rules.append(ForEachPlayer(player_type, give_5_cards))
    phase_start.rules.append(ChangePhase(phase1, firstPlayer))

    #faza - wybor gracza
    phase_choose_player.rules.append(ChangePhase(phase1, nextPlayer))
    phase_win_check.rules.append(WinCheck(phase_choose_player, phase_end))

    #faza - tura gracza
    #Place, Place, Artifacts -> bool
    sums_to_5_10_15 = lambda from_place, to_place, moved_cards: moved_cards.ranks_sum() in [5,10,15]
    #w makao bedzie coś w stylu moved_cards[0].color == to_place.top_card.color

    #coś wtym stylu
    CURRENT_PLAYER = current_player_for_type(player_type)
    CURRENT_PLAYER = SelectPlayer.CurrentPlayer #FOO('current-player')
    phase1.rules.append(Move(CURRENT_PLAYER, player_hand, TABLE_PLAYER, discard_pile, number_of_cards='any?', condition=sums_to_5_10_15))
    phase1.rules.append(ChangePhase(phase_win_check, TABLE_PLAYER))

    return game





