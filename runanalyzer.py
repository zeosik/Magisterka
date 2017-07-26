import logging, argparse

from common.initlogger import initloggerconfiguration
from simulator import simulatorengine

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--num_players", help="Ilosc graczy", type=int, default=3)
    parser.add_argument("-g", "--game_name", help="Nazwa gry do uruchomienia", type=str, choices=["5_10_15", "5_10_15_one_phase", "card_sequence"], default="5_10_15")
    parser.add_argument("-s", "--num_simulations", help="Ilosc symulacji", type=int, default=10)

    args = parser.parse_args()

    initloggerconfiguration(False)

    for n in range(args.num_simulations):
        print()
        print("Iteracja:", n + 1)
        print()
        simulatorengine.run(args.game_name, args.num_players, 0)

    #Analizujemy gre dla konkretnej liczby graczy, czy sprawdzamy jak się zachowuje gdy graczy jest mniej i wiecej?

    #CO ANALIZOWAĆ - POMYSŁY:
    # - liczba tur w każdej grze - czy jest ich dużo czy mało
    # - liczba tur w każdej grze - jak bardzo się wacha w zależności od kart
    # - średnia ilość wszystkich ruchów w turze
    # - średnia ilość dozwolonych ruchów w turze
    # - kto wygrywa (może gra jest nie fair i np pierwszy gracz ma łatwiej)
    # - procent wykorzystanych kart (ila kart zostało nieodkrytych) - tylko po co to nam? :P