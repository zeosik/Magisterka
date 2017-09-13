import logging, argparse

from common.initlogger import initloggerconfiguration
from simulator import simulatorengine

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--num_players", help="Ilosc graczy", type=int, default=3)
    parser.add_argument("-f", "--num_humans", help="Ilosc fizycznych graczy", type=int, default=0)
    parser.add_argument("-r", "--num_random_bots", help="Ilosc botow grajacyh losowo", type=int, default=0)
    parser.add_argument("-d", "--debug", help="Wypisz informacje debugowe", action='store_true')
    parser.add_argument("-g", "--game_name", help="Nazwa gry do uruchomienia", type=str, choices=["5_10_15", "5_10_15_one_phase", "card_sequence", "remik"], default="5_10_15")

    args = parser.parse_args()

    if (args.debug):
        initloggerconfiguration(logging.DEBUG)
    else:
        initloggerconfiguration(logging.INFO)

    simulatorengine.run(args.game_name, args.num_players, args.num_humans, args.num_random_bots)