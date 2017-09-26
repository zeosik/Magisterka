from common.articaft_generators.cardgenerator import CardGenerator
from common.gamecreator import GameCreator
from common.model.cardpicker.duplicaterankcardpicker import DuplicateRankCardPicker
from common.model.cardpicker.topcardfillpicker import TopCardFillPicker
from common.model.cardpicker.allcardpicker import AllCardPicker
from common.model.conditions.artifactsinplaceequal import ArtifactsInPlaceEqual
from common.model.conditions.artifactsinplacelessthen import ArtifactsInPlaceLessThen
from common.model.conditions.emptyplace import EmptyPlace
from common.model.conditions.ifnot import IfNot
from common.model.conditions.ifnumberofplayers import IfNumberOfPlayers
from common.model.conditions.iscurrentplayerinphase import IsCurrentPlayerInPhase
from common.model.conditions.moveconditions.numberofmovedartifacts import NumberOfMovedArtifacts
from common.model.conditions.newround import NewRound
from common.model.placepicker.lastgroupplacepicker import LastGroupPlacePicker
from common.model.places.place import Place
from common.model.places.placegroup import PlaceGroup
from common.model.playerchooser.currentplayerchooser import CurrentPlayerChooser
from common.model.playerchooser.firstplayerchooser import FirstPlayerChooser
from common.model.playerchooser.nextplayerchooser import NextPlayerChooser
from common.model.playerchooser.tableplayerchooser import TablePlayerChooser
from common.model.artifacts.card import CardColor
from common.model.cardpicker.cardpicker import CardPicker
from common.model.cardpicker.topcardpicker import TopCardPicker
from common.model.conditions.moveconditions.cardssumsto import CardsSumsTo
from common.model.gamemodel import GameModel
from common.model.phase import Phase
from common.model.placepicker.placepicker import PlacePicker
from common.model.places.cardline import PlayerCardLine, FaceUpCardLine
from common.model.places.cardpile import FaceDownCardPile, FaceUpCardPile
from common.model.playertype import PlayerType
from common.model.rules.passrule import Pass
from common.model.rules.changephase import ChangePhase
from common.model.rules.foreachplayer import ForEachPlayer
from common.model.rules.ifrule import If
from common.model.rules.move import Move
from common.model.rules.preparenewplaceinplacegroup import PrepareNewPlaceInPlaceGroup
from common.model.rules.shuffle import Shuffle


def example_5_10_15(two_phase: bool = True) -> GameModel:

    game = GameModel('5-10-15')
    game.time_per_move = 5

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
    phase_start = table_type.add_phase(Phase('przygotowanie planszy'))
    game.start_phase = phase_start
    phase_end = table_type.add_phase(Phase('koniec gry'))
    game.end_phase = phase_end
    phase_choose_player = table_type.add_phase(Phase('choose-player'))
    phase_win_check = table_type.add_phase(Phase('win-check'))
    if two_phase:
        phase1 = player_type.add_phase(Phase('Tura zagrywania kart'))
        phase2_draw = player_type.add_phase(Phase('Tura dobierania kart'))
    else:
        phase1 = player_type.add_phase(Phase('Tura zagrywania kart'))

    #faza - rozdanie poczatkowe

    phase_start.append_rule(Shuffle(PlacePicker(TablePlayerChooser(), deck)))
    #Player -> Rule
    give_5_cards = lambda playerChooser: Move(TopCardPicker(5, PlacePicker(TablePlayerChooser(), deck), PlacePicker(playerChooser, player_hand)))
    phase_start.rules[0].append_next(ForEachPlayer(player_type, give_5_cards))
    phase_start.rules[0].next[0].append_next(ChangePhase(phase1, FirstPlayerChooser(player_type)))

    #faza - wybor gracza
    if two_phase:
        to_player_turn_phase1 = ChangePhase(phase1, NextPlayerChooser(CurrentPlayerChooser(player_type)))
        to_player_turn_phase2 = ChangePhase(phase2_draw, NextPlayerChooser(CurrentPlayerChooser(player_type)))
        to_player_turn_when_phase1 = If(NewRound(player_type), to_player_turn_phase2, to_player_turn_phase1)
        to_player_turn_when_phase2 = If(NewRound(player_type), to_player_turn_phase1, to_player_turn_phase2)
        to_player_turn = If(IsCurrentPlayerInPhase(phase1, player_type), to_player_turn_when_phase1, to_player_turn_when_phase2)
    else:
        to_player_turn = ChangePhase(phase1, NextPlayerChooser(CurrentPlayerChooser(player_type)))

    reshuffle_deck_rule = Move(AllCardPicker(PlacePicker(TablePlayerChooser(), discard_pile), PlacePicker(TablePlayerChooser(), deck)))
    reshuffle_deck_rule.append_next(Shuffle(PlacePicker(TablePlayerChooser(), deck)))
    reshuffle_deck_rule.next[0].append_next(to_player_turn)
    phase_choose_player.append_rule(If(EmptyPlace(PlacePicker(TablePlayerChooser(), deck)), reshuffle_deck_rule, to_player_turn))

    #faza - sprawdzenie wygranej
    win_condition = IfNumberOfPlayers(1, player_type, lambda p: IfNot(EmptyPlace(PlacePicker(p, player_hand))))
    phase_win_check.append_rule(If(win_condition, ChangePhase(phase_end, TablePlayerChooser()) , ChangePhase(phase_choose_player, TablePlayerChooser())))
 
    #faza - tura gracza
    source_place_picker = PlacePicker(CurrentPlayerChooser(player_type), player_hand)
    target_place_picker = PlacePicker(TablePlayerChooser(), discard_pile)
    card_picker = CardPicker(source_place_picker, target_place_picker)
    card_picker.add_condition(CardsSumsTo([5, 10, 15]))
    play_cards = Move(card_picker)
    play_cards.user_name_str = "Zagraj karty"
    phase1.append_rule(play_cards)

    take_card_from_deck = Move(TopCardPicker(1, PlacePicker(TablePlayerChooser(), deck), PlacePicker(CurrentPlayerChooser(player_type), player_hand)))
    take_card_from_deck.user_name_str = "Dobierz kartę"
    if two_phase:
        passs = Pass()
        passs.user_name_str = "Spasuj"
        phase1.append_rule(passs)
    else:
        phase1.append_rule(take_card_from_deck)
    phase1_endturn = ChangePhase(phase_win_check, TablePlayerChooser())
    phase1_endturn.user_name_str = 'Koniec tury'
    phase1.rules[0].append_next(phase1_endturn)
    phase1.rules[1].append_next(phase1_endturn)

    #phase2-draw
    if two_phase:
        phase2_draw.append_rule(take_card_from_deck)
        phase2_end_turn = ChangePhase(phase_choose_player, TablePlayerChooser())
        phase2_end_turn.user_name_str = "Koniec tury"
        phase2_draw.rules[0].append_next(phase2_end_turn)

    return game


def example_card_sequence():
    game = GameModel('dwie pary')
    game.time_per_move = 5

    table_type = game.add_table_type(PlayerType('table-type'))
    player_type = game.add_player_type(PlayerType('player-type'))

    # rekwizyty
    cards = CardGenerator.cards(1, 10, list(CardColor))

    #miejsca
    middle = table_type.add_place(FaceUpCardLine('środek'))
    deck = table_type.add_place(FaceDownCardPile('talia', cards))
    discard = table_type.add_place(FaceDownCardPile('odrzucone'))
    points = player_type.add_place(FaceDownCardPile('zdobyte'))

    #fazy stolu
    start_phase = table_type.add_phase(Phase('przygotowania rozgrywki'))
    refill_middle_phase = table_type.add_phase(Phase('uzupełnienia środka'))
    move_duplicates_phase = table_type.add_phase(Phase('odrzucenia dupliaktów'))
    win_check_phase = table_type.add_phase(Phase('sprawdzenia wygranej'))
    choose_player_phase = table_type.add_phase(Phase('wybóru następnego gracza'))
    end_phase = table_type.add_phase(Phase('koniec gry'))

    game.start_phase = start_phase
    game.end_phase = end_phase

    #table_place_pickers
    middle_picker = PlacePicker(TablePlayerChooser(), middle)
    deck_picker = PlacePicker(TablePlayerChooser(), deck)
    discard_picker = PlacePicker(TablePlayerChooser(), discard)

    #fazy graczy
    player_phase = player_type.add_phase(Phase('tury gracza'))

    #start_phase
    sp_shuffle = Shuffle(PlacePicker(TablePlayerChooser(), deck))
    sp_shuffle.user_name_str = "potasuj talie"
    start_phase.append_rule(sp_shuffle)
    fill_middle_to_8_cards = Move(TopCardFillPicker(8, PlacePicker(TablePlayerChooser(), deck), PlacePicker(TablePlayerChooser(), middle)))
    fill_middle_to_8_cards.user_name_str = 'Uzupełnij karty na środku'
    start_phase.rules[0].append_next(fill_middle_to_8_cards)
    sp_end_turn = ChangePhase(player_phase, FirstPlayerChooser(player_type))
    sp_end_turn.user_name_str = 'tura pierwszego gracza'
    start_phase.rules[0].next[0].append_next(sp_end_turn)

    #refill middle
    full_middle = ArtifactsInPlaceEqual(8, PlacePicker(TablePlayerChooser(), middle))
    move_middle_to_discard = Move(TopCardPicker(8, PlacePicker(TablePlayerChooser(), middle), PlacePicker(TablePlayerChooser(), discard)))
    less_then_8_cards_in_deck = ArtifactsInPlaceLessThen(8, PlacePicker(TablePlayerChooser(), deck))
    move_discard_to_deck = Move(AllCardPicker(discard_picker, deck_picker))
    shuffle_deck = Shuffle(deck_picker)
    shuffle_deck.user_name_str = "potasuj talie"
    move_discard_to_deck.append_next(shuffle_deck)
    move_discard_to_deck.user_name_str = "przenieś odrzucone do talia"
    fill_middle_cards = Move(TopCardFillPicker(8, deck_picker, middle_picker))
    fill_middle_cards.user_name_str = "Przenieś 8 kart na środek"
    shuffle_deck.append_next(fill_middle_cards)
    check_if_shuffle_deck = If(less_then_8_cards_in_deck, move_discard_to_deck, fill_middle_cards)
    check_if_shuffle_deck.user_name_str = "czy w talii jest mniej niż 8 kart"
    move_middle_to_discard.append_next(check_if_shuffle_deck)
    move_middle_to_discard.user_name_str = 'odrzuć karty ze środka'
    fill_middle_cards.append_next(ChangePhase(choose_player_phase, TablePlayerChooser()))
    fill_middle_cards.next[0].user_name_str = "wybór następnego gracza"
    refill_middle_phase.append_rule(If(full_middle, move_middle_to_discard, check_if_shuffle_deck))
    refill_middle_phase.rules[0].user_name_str = 'czy na środku jest 8 kart'

    #move duplicates
    move_duplicates_phase.append_rule(Move(DuplicateRankCardPicker(PlacePicker(CurrentPlayerChooser(player_type), points), PlacePicker(TablePlayerChooser(), discard))))
    move_duplicates_phase.rules[0].user_name_str = "Przenieś duplikaty"
    move_duplicates_phase.rules[0].append_next(ChangePhase(win_check_phase, TablePlayerChooser()))
    move_duplicates_phase.rules[0].next[0].user_name_str = 'Sprawdzanie wygranej'

    #win check
    to_choose_player = ChangePhase(refill_middle_phase, TablePlayerChooser())
    to_choose_player.user_name_str = "uzupełnij środek"
    to_end_game = ChangePhase(end_phase, TablePlayerChooser())
    to_end_game.user_name_str = 'koniec gry'
    has_10_cards = ArtifactsInPlaceEqual(10, PlacePicker(CurrentPlayerChooser(player_type), points))
    win_check_phase.append_rule(If(has_10_cards, to_end_game, to_choose_player))
    win_check_phase.rules[0].user_name_str = "Czy obecny gracz ma 10 kart"

    #choose player
    choose_player_phase.append_rule(ChangePhase(player_phase, NextPlayerChooser(CurrentPlayerChooser(player_type))))
    choose_player_phase.rules[0].user_name_str = "tura następnego gracza"

    #player_phase
    p_card_picker = CardPicker(PlacePicker(TablePlayerChooser(), middle), PlacePicker(CurrentPlayerChooser(player_type), points))
    p_card_picker.add_condition(CardsSumsTo([10]))
    #p_card_picker.add_condition(NumberOfMovedArtifacts(2))
    pp_move = Move(p_card_picker)
    pp_move.user_name_str = 'dobierz karty'
    player_phase.append_rule(pp_move)
    pp_pass = Pass()
    pp_pass.user_name_str = "spasuj"
    player_phase.append_rule(pp_pass)
    end_turn = ChangePhase(move_duplicates_phase, TablePlayerChooser())
    end_turn.user_name_str = "koniec tury"
    player_phase.rules[0].append_next(end_turn)
    player_phase.rules[1].append_next(end_turn)

    return game

#TODO moze jakies anotacje i szukanie gier po anotacjach albo pobieranie z jakiegos folderu
def example_remik() -> GameModel:
    #TODO max players 3 na talie?
    game = GameModel('remik')
    game.time_per_move = 10

    #typy
    table_type = game.add_table_type(PlayerType('table-type'))
    player_type = game.add_player_type(PlayerType('player-type'))

    # rekwizyty
    cards = CardGenerator.cards_standard_52()

    # miejsca
    deck = table_type.add_place(FaceDownCardPile('deck', cards))
    discard = table_type.add_place(FaceUpCardPile('discard'))

    deck_picker = PlacePicker(TablePlayerChooser(), deck)
    discard_picker = PlacePicker(TablePlayerChooser(), discard)

    hand = player_type.add_place(PlayerCardLine('hand'))
    hand_current_player_picker = PlacePicker(CurrentPlayerChooser(player_type), hand)

    played_cards_template = PlayerCardLine('played_cards')
    played_cards = PlaceGroup(played_cards_template)
    player_type.add_place(played_cards)


    # fazy stołu
    start = table_type.add_phase(Phase('start'))
    win_check = table_type.add_phase(Phase('victory check'))
    choose_player = table_type.add_phase(Phase('choose-player'))
    end = table_type.add_phase(Phase('end'))

    game.start_phase = start
    game.end_phase = end

    # fazy graczy
    play = player_type.add_phase(Phase('play'))

    #start
    start.append_rule(Shuffle(deck_picker))
    start.rules[0].append_next(ForEachPlayer(player_type, give_n_cards(13, deck_picker, hand)))
    start.rules[0].next[0].append_next(ChangePhase(play, FirstPlayerChooser(player_type)))

    #win check
    to_end_game = ChangePhase(end, TablePlayerChooser())
    to_choose_player = ChangePhase(choose_player, TablePlayerChooser())
    win_check.append_rule(If(EmptyPlace(PlacePicker(CurrentPlayerChooser(player_type), hand)), to_end_game, to_choose_player))

    #choose player
    choose_player.append_rule(ChangePhase(play, NextPlayerChooser(CurrentPlayerChooser(player_type))))

    #end

    #play
    take_card_from_deck = Move(TopCardPicker(1, deck_picker, hand_current_player_picker))
    play.append_rule(take_card_from_deck)
    end_turn = ChangePhase(win_check, TablePlayerChooser())
    discard_card_card_picker = CardPicker(hand_current_player_picker, discard_picker)
    discard_card_card_picker.add_condition(NumberOfMovedArtifacts(1))
    discard_card = Move(discard_card_card_picker)
    discard_card.append_next(end_turn)
    create_new_pile = PrepareNewPlaceInPlaceGroup(PlacePicker(CurrentPlayerChooser(player_type), played_cards))
    create_new_pile_card_picker = CardPicker(hand_current_player_picker, LastGroupPlacePicker(CurrentPlayerChooser(player_type), played_cards))
    #card_picker.add_condition()
    create_new_pile.append_next(Move(create_new_pile_card_picker))
    create_new_pile.next[0].append_next(discard_card)


    take_card_from_deck.append_next(create_new_pile)

    take_card_from_deck.append_next(discard_card)

    return game


def give_n_cards(number: int, table_place_picker: PlacePicker, player_place: Place):
    return lambda player_picker: Move(TopCardPicker(number, table_place_picker, PlacePicker(player_picker, player_place)))


def testfoo() -> GameModel:
    game = GameCreator('test')

    cards = CardGenerator.cards(1, 1, list(CardColor))

    table, table_chooser, table_creator = game.add_table_type()
    player, player_chooser, player_creator = game.add_player_type("players")

    start_phase = table_creator.add_start_phase('przygotowanie planszy')
    end_phase = table_creator.add_end_phase('koniec gry')
    table_turn = table_creator.add_phase('tura stołu')

    play_phase = player_creator.add_phase('tura zagrywania kart')
    draw_phase = player_creator.add_phase('tura dobierania kart')

    deck, deck_picker = table_creator.add_place('Talia')
    deck._artifacts = cards
    discard, discard_picker = table_creator.add_place('Środek')
    hand, hand_picker = player_creator.add_place("Ręka")

    shuffle_deck = Shuffle(deck_picker)
    shuffle_deck.user_name_str = "Potasuj talie"

    to_table_turn = ChangePhase(table_turn, table_chooser)

    give_cards = ForEachPlayer(player, give_n_cards(5, deck_picker, hand))
    give_cards.user_name_str = 'Dla każdego gracza'
    give_cards.dummy_actions[0].user_name_str = 'Przenieś 5 kart z talia do ręka gracza'
    #start_phase.append_rule(sequence([shuffle_deck, give_cards, to_table_turn]))

    m1 = Move(AllCardPicker(deck_picker, discard_picker))
    m2 = Move(AllCardPicker(discard_picker, deck_picker))
    start_phase.append_rule(sequence([m1, m2, ChangePhase(start_phase, TablePlayerChooser())]))

    return game.model


def test2() -> GameModel:
    game = GameModel("5-10-15-test")

    table = game.add_table_type(PlayerType('table'))
    p1 = game.add_player_type(PlayerType('gracz 1'))
    p2 = game.add_player_type(PlayerType('gracz 2'))

    p1_picker = CurrentPlayerChooser(p1)
    p2_picker = CurrentPlayerChooser(p2)

    deck = table.add_place(FaceDownCardPile('Talia'))
    deck_picker = PlacePicker(TablePlayerChooser(), deck)
    discard = table.add_place(FaceUpCardPile('Środek'))
    discard_picker = PlacePicker(TablePlayerChooser(), discard)

    p1_hand = p1.add_place(PlayerCardLine('Ręka pierwszego gracza'))
    p1_hand_picker = PlacePicker(p1_picker, p1_hand)
    p2_hand = p2.add_place(PlayerCardLine('Ręka drugiego gracza'))
    p2_hand_picker = PlacePicker(p2_picker, p2_hand)

    p1_turn = p1.add_phase(Phase('Tura zagrywania kart'))
    p2_turn = p2.add_phase(Phase('Tura dobierania kart'))



    start = table.add_phase(Phase('Przygotowanie gry'))
    end = table.add_phase(Phase('Koniec gry'))
    table_turn = table.add_phase(Phase('Tura stołu'))

    shuffle = Shuffle(deck_picker)
    shuffle.user_name_str = 'Potasuj talie'
    give_5_card_to_p1 = give_n_cards(5, deck_picker, p1_hand)(p1_picker)
    give_5_card_to_p1.user_name_str = 'Przełóż 5 kart z talia do ręka pierwszego gracza'
    give_5_card_to_p2 = give_n_cards(5, deck_picker, p2_hand)(p2_picker)
    give_5_card_to_p2.user_name_str = 'Przełóż 5 kart z talia do ręka drugiego gracza'

    to_p1_turn = ChangePhase(p1_turn, p1_picker)
    to_p1_turn.user_name_str = 'Tura zagrywania kart'
    to_p2_turn = ChangePhase(p2_turn, p2_picker)
    to_p2_turn.user_name_str = 'Tura dobierania kart'
    end_game = ChangePhase(end, TablePlayerChooser())
    end_game.user_name_str = 'Koniec gry'

    give_cards = ForEachPlayer(p1, give_n_cards(5, deck_picker, p1_hand))
    give_cards.user_name_str = 'Dla każdego gracza'
    give_cards.dummy_actions[0].user_name_str = 'Przenieś 5 kart z talia do ręka gracza'

    #start.append_rule(sequence([shuffle, give_5_card_to_p1, give_5_card_to_p2, to_p1_turn]))
    start.append_rule(sequence([shuffle, give_cards, to_p1_turn]))

    p1_play_card = Move(CardPicker(p1_hand_picker, discard_picker))
    p1_play_card.user_name_str = ' Zagraj karty'
    p1_play_card.card_picker.add_condition(CardsSumsTo([5, 10, 15]))
    p1_take_card = Move(TopCardPicker(1, deck_picker, p1_hand_picker))
    p1_take_card.user_name_str = 'Dobierz kartę'
    #p1_if = If(EmptyPlace(p1_hand_picker), end_game, to_p2_turn)
    #p1_if.user_name_str = 'Czy koniec gry'
    to_table_turn = ChangePhase(table_turn, TablePlayerChooser())
    to_table_turn.user_name_str = 'Koniec tury'

    sequence([p1_play_card, to_table_turn])
    sequence([p1_take_card, to_table_turn])
    p1_turn.append_rule(p1_play_card)
    p1_turn.append_rule(p1_take_card)

    p2_play_card = Move(CardPicker(p2_hand_picker, discard_picker))
    p2_play_card.user_name_str = ' Zagraj karty'
    p2_play_card.card_picker.add_condition(CardsSumsTo([5, 10, 15]))
    p2_take_card = Move(TopCardPicker(1, deck_picker, p2_hand_picker))
    p2_take_card.user_name_str = 'Dobierz kartę'
    p2_if = If(EmptyPlace(p2_hand_picker), end_game, to_table_turn)
    p2_if.user_name_str = 'Czy koniec gry'

    sequence([p2_play_card, to_table_turn])
    sequence([p2_take_card, to_table_turn])
    p2_turn.append_rule(p2_play_card)
    p2_turn.append_rule(p2_take_card)

    game.start_phase = start
    game.end_phase = end

    to_player_turn_phase1 = ChangePhase(p1_turn, NextPlayerChooser(CurrentPlayerChooser(p1)))
    to_player_turn_phase1.user_name_str = 'Tura zagrywania kart następnego gracza'
    to_player_turn_phase2 = ChangePhase(p2_turn, NextPlayerChooser(CurrentPlayerChooser(p2)))
    to_player_turn_phase2.user_name_str = 'Tura dobierania kart następnego gracza'
    to_player_turn_when_phase1 = If(NewRound(p1), to_player_turn_phase2, to_player_turn_phase1)
    to_player_turn_when_phase1.user_name_str = "Czy rozpocząć nową kolejke"
    to_player_turn_when_phase2 = If(NewRound(p1), to_player_turn_phase1, to_player_turn_phase2)
    to_player_turn_when_phase2.user_name_str = "Czy rozpocząć nową kolejke"
    to_player_turn = If(IsCurrentPlayerInPhase(p1_turn, p1), to_player_turn_when_phase1,
                        to_player_turn_when_phase2)
    to_player_turn.user_name_str = "Czy ostatnio była tura zagrywania kart"

    #p1_win_check = If(EmptyPlace(p1_hand_picker), end_game, to_p1_turn)
    #p1_win_check.user_name_str = "Czy ręka pierwszego gracza jest pusta"
    #p2_win_check = If(EmptyPlace(p2_hand_picker), end_game, to_p2_turn)
    #p2_win_check.user_name_str = "Czy ręka drugiego gracza jest pusta"
    #if_win_check = If(NewRound(p1), p1_win_check, p2_win_check)
    #if_win_check.user_name_str = 'Czy ostatnio był gracz 2'
    #if_win_check = If(EmptyPlace(p1_hand_picker), end_game, to_p2_turn)
    if_win_check = If(EmptyPlace(p1_hand_picker), end_game, to_player_turn)
    if_win_check.user_name_str = "Czy liczba graczy z pustą ręką jest równa 1"
    to_p2_turn.user_name_str = "Tura następnego gracza"
    shuffle2 = Move(AllCardPicker(discard_picker, deck_picker))
    shuffle2.user_name_str = 'Przenieś środek do talia'
    shuffle3 = Shuffle(deck_picker)
    shuffle3.user_name_str = 'Potasuj talia'
    sequence([shuffle2, shuffle3, if_win_check])
    if_shuffle = If(EmptyPlace(deck_picker), shuffle2, if_win_check)
    if_shuffle.user_name_str = 'Czy talia jest pusta'

    table_turn.append_rule(if_shuffle)

    return game

def sequence(rules: list):
    for i in range(1, len(rules)):
        r1 = rules[i - 1]
        r2 = rules[i]
        r1.append_next(r2)
    return rules[0]
