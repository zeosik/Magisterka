from common.articaft_generators.cardgenerator import CardGenerator
from common.model.conditions.emptyplace import EmptyPlace
from common.model.conditions.iscurrentplayerinphase import IsCurrentPlayerInPhase
from common.model.conditions.newround import NewRound
from common.model.playerchooser.currentplayerchooser import CurrentPlayerChooser
from common.model.playerchooser.firstplayerchooser import FirstPlayerChooser
from common.model.playerchooser.nextplayerchooser import NextPlayerChooser
from common.model.playerchooser.tableplayerchooser import TablePlayerChooser
from common.model.artifacts.card import CardColor
from common.model.cardpicker.cardpicker import CardPicker
from common.model.cardpicker.topcardpicker import TopCardPicker
from common.model.conditions.ifcounter import IfCounter
from common.model.conditions.moveconditions.cardssumsto import CardsSumsTo
from common.model.gamemodel import GameModel
from common.model.phase import Phase
from common.model.placepicker.placepicker import PlacePicker
from common.model.places.cardline import PlayerCardLine
from common.model.places.cardpile import FaceDownCardPile, FaceUpCardPile
from common.model.playertype import PlayerType
from common.model.rules.passrule import Pass
from common.model.rules.changephase import ChangePhase
from common.model.rules.foreachplayer import ForEachPlayer
from common.model.rules.ifrule import If
from common.model.rules.move import Move
from common.model.rules.shuffle import Shuffle


def example_5_10_15():

    game = GameModel('5-10-15')

    #
    table_type = game.add_table_type(PlayerType('table-type'))
    player_type = game.add_player_type(PlayerType('players'))
    player_type.min_players = 2
    player_type.max_players = 10

    # rekwizyty
    cards = CardGenerator.cards(min_rank=1, max_rank=10, colors=list(CardColor))

    #miejsca
    player_hand = player_type.add_place(PlayerCardLine('hand'))
    deck = table_type.add_place(FaceDownCardPile('deck', starting_artifacts=cards))
    discard_pile = table_type.add_place(FaceUpCardPile('discard pile'))

    #fazy
    phase_start = table_type.add_phase(Phase('start'))
    game.start_phase = phase_start
    phase_end = table_type.add_phase(Phase('end'))
    game.end_phase = phase_end
    phase_choose_player = table_type.add_phase(Phase('choose-player'))
    phase_win_check = table_type.add_phase(Phase('win-check'))
    phase1 = player_type.add_phase(Phase('phase1'))
    phase2_draw = player_type.add_phase(Phase('phase2-draw'))

    #faza - rozdanie poczatkowe

    phase_start.append_rule(Shuffle(PlacePicker(TablePlayerChooser(), deck)))
    #Move(from_player_type, from_player_in_this_type, from_pile_in_this_player, to_player_type, to_player, to_pile)
    #Player -> Rule
    #give_5_cards = lambda playerChooser: OldMove(TablePlayerChooser(), deck, playerChooser, player_hand, TopCardPickerOld(5))
    give_5_cards = lambda playerChooser: Move(TopCardPicker(5, PlacePicker(TablePlayerChooser(), deck), PlacePicker(playerChooser, player_hand)))
    phase_start.rules[0].append_next(ForEachPlayer(player_type, give_5_cards))
    phase_start.rules[0].next[0].append_next(ChangePhase(phase1, FirstPlayerChooser(player_type)))

    #faza - wybor gracza
    to_player_turn_phase1 = ChangePhase(phase1, NextPlayerChooser(CurrentPlayerChooser(player_type)))
    to_player_turn_phase2 = ChangePhase(phase2_draw, NextPlayerChooser(CurrentPlayerChooser(player_type)))
    to_player_turn_when_phase1 = If(NewRound(player_type), to_player_turn_phase2, to_player_turn_phase1)
    to_player_turn_when_phase2 = If(NewRound(player_type), to_player_turn_phase1, to_player_turn_phase2)
    to_player_turn = If(IsCurrentPlayerInPhase(phase1, player_type), to_player_turn_when_phase1, to_player_turn_when_phase2)
    phase_choose_player.append_rule(to_player_turn)
    phase_win_check.append_rule(If(EmptyPlace(PlacePicker(CurrentPlayerChooser(player_type), player_hand)), ChangePhase(phase_end, TablePlayerChooser()) , to_player_turn))
    #phase_win_check.append_rule(If(IfCounter(3), to_player_turn, ChangePhase(phase_end, TablePlayerChooser())))

    #faza - tura gracza
    #Place, Place, Artifacts -> bool
    sums_to_5_10_15 = lambda from_place, to_place, moved_cards: moved_cards.ranks_sum() in [5,10,15]
    #w makao bedzie coś w stylu moved_cards[0].color == to_place.top_card.color


    source_place_picker = PlacePicker(CurrentPlayerChooser(player_type), player_hand)
    target_place_picker = PlacePicker(TablePlayerChooser(), discard_pile)
    picp = CardPicker(source_place_picker, target_place_picker, CardsSumsTo([5, 10, 15]))
    #phase1.rule = Move(CurrentPlayerChooser(player_type), player_hand, TablePlayerChooser(), discard_pile, PlayerInputCardPicker("any"), condition=sums_to_5_10_15)
    phase1.append_rule(Move(picp))

    take_card_from_deck = Move(TopCardPicker(1, PlacePicker(TablePlayerChooser(), deck), PlacePicker(CurrentPlayerChooser(player_type), player_hand)))
    phase1.append_rule(Pass())
    #phase1.append_rule(take_card_from_deck)
    phase1_endturn = ChangePhase(phase_win_check, TablePlayerChooser())
    phase1.rules[0].append_next(phase1_endturn)
    phase1.rules[1].append_next(phase1_endturn)

    #phase2-draw
    phase2_draw.append_rule(take_card_from_deck)
    phase2_end_turn = ChangePhase(phase_choose_player, TablePlayerChooser())
    phase2_draw.rules[0].append_next(phase2_end_turn)

    return game





