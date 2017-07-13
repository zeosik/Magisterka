from common.articaft_generators.cardgenerator import CardGenerator
from common.model.PlayerChooser.currentplayerchooser import CurrentPlayerChooser
from common.model.PlayerChooser.firstplayerchooser import FirstPlayerChooser
from common.model.PlayerChooser.nextplayerchooser import NextPlayerChooser
from common.model.PlayerChooser.tableplayerchooser import TablePlayerChooser
from common.model.cardpicker.cardpicker import CardPicker
from common.model.cardpicker.topcardpicker import TopCardPicker
from common.model.cardpicker.playerinputpicker import PlayerInputPicker
from common.model.artifacts.card import CardColor
from common.model.conditions.ifcounter import IfCounter
from common.model.gamemodel import GameModel
from common.model.phase import Phase
from common.model.places.cardpile import FaceDownCardPile, FaceUpCardPile
from common.model.places.cardline import PlayerCardLine
from common.model.playertype import PlayerType
from common.model.player import Player
from common.model.rules.changephase import ChangePhase
from common.model.rules.ifrule import If
from common.model.rules.foreachplayer import ForEachPlayer
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

    #faza - rozdanie poczatkowe

    phase_start.rules.append(Shuffle(TablePlayerChooser(), deck))
    #Move(from_player_type, from_player_in_this_type, from_pile_in_this_player, to_player_type, to_player, to_pile)
    #Player -> Rule
    give_5_cards = lambda playerChooser: Move(TablePlayerChooser(), deck, playerChooser, player_hand, TopCardPicker(5))
    phase_start.rules.append(ForEachPlayer(player_type, give_5_cards))
    phase_start.rules.append(ChangePhase(phase1, FirstPlayerChooser(player_type)))

    #faza - wybor gracza
    to_player_turn = ChangePhase(phase1, NextPlayerChooser(CurrentPlayerChooser(player_type)))
    phase_choose_player.rules.append(to_player_turn)
    phase_win_check.rules.append(If(IfCounter(3), to_player_turn, ChangePhase(phase_end, TablePlayerChooser())))

    #faza - tura gracza
    #Place, Place, Artifacts -> bool
    sums_to_5_10_15 = lambda from_place, to_place, moved_cards: moved_cards.ranks_sum() in [5,10,15]
    #w makao bedzie coś w stylu moved_cards[0].color == to_place.top_card.color

    phase1.rules.append(Move(CurrentPlayerChooser(player_type), player_hand, TablePlayerChooser(), discard_pile, PlayerInputPicker("any"), condition=sums_to_5_10_15))
    phase1.rules.append(ChangePhase(phase_win_check, TablePlayerChooser()))

    return game





