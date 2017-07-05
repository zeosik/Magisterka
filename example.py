from common.articaft_generators.cardgenerator import CardGenerator
from common.model.artifacts.card import CardColor
from common.model.gamemodel import GameModel
from common.model.phase import Phase
from common.model.places.place import Place
from common.model.playertype import PlayerType


def example_5_10_15():

    game = GameModel('5-10-15')

    #
    table_type = game.add_table_type(PlayerType('table-type'))
    player_type = game.add_player_type(PlayerType('players'))
    player_type.min_players = 2
    player_type.max_players = 10

    #?
    TABLE_PLAYER = None

    # rekwizyty
    cards = CardGenerator.cards(min_rank=1, max_rank=10, colors=list(CardColor))

    #miejsca
    player_hand = player_type.add_place(Place('hand'))
    deck = table_type.add_place(Place('deck', starting_artifacts=cards))
    discard_pile = table_type.add_place(Place('discard pile'))

    #fazy
    phase_start = table_type.add_phase(Phase('start'))
    game.start_phase = phase_start
    phase_choose_player = table_type.add_phase(Phase('choose-player'))
    phase1 = player_type.add_phase(Phase('phase1'))

    #faza - rozdanie poczatkowe
    #list<Player>, int -> int
    #Może jakas klasa? PlayerChoose?
    firstPlayer = lambda players_list, current_index: 1
    nextPlayer = lambda players_list, current_index: (current_index + 1) % len(players_list)

    phase_start.rule = Shuffle(TABLE_PLAYER, deck)
    #Move(from_player_type, from_player_in_this_type, from_pile_in_this_player, to_player_type, to_player, to_pile)
    #Player -> Rule
    give_5_cards = lambda player: Move(TABLE_PLAYER, deck, player, player_hand, number_of_cards=5)
    phase_start.rule.next = ForEachPlayer(in_player_type = player_type).Do(action=give_5_cards)
    phase_start.rule.next.next = ToPlayerPhase(phase1, firstPlayer)

    #faza - wybor gracza
    phase_choose_player.rule = ToPlayerPhase(phase1, nextPlayer)

    #faza - tura gracza
    #Place, Place, Artifacts -> bool
    sums_to_5_10_15 = lambda from_place, to_place, moved_cards: moved_cards.ranks_sum() in [5,10,15]
    #w makao bedzie coś w stylu moved_cards[0].color == to_place.top_card.color

    #coś wtym stylu
    CURRENT_PLAYER = current_player_for_type(player_type)
    phase1.rule = Move(CURRENT_PLAYER, player_hand, TABLE_PLAYER, discard_pile, number_of_cards='any?', condition=sums_to_5_10_15)
    phase1.rule.next = EndTurn(phase_choose_player)





