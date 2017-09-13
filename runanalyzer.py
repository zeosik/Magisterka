import logging, argparse

from common.initlogger import initloggerconfiguration
from analyzer import analyzer

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--num_players", help="Ilosc graczy", type=int, default=3)
    parser.add_argument("-r", "--num_random_bots", help="Ilosc botow grajacyh losowo", type=int, default=0)
    parser.add_argument("-g", "--game_name", help="Nazwa gry do uruchomienia", type=str, choices=["5_10_15", "5_10_15_one_phase", "card_sequence"], default="5_10_15")
    parser.add_argument("-s", "--num_simulations", help="Ilosc symulacji", type=int, default=10)

    args = parser.parse_args()

    initloggerconfiguration(logging.ERROR)

    analyzer.run(args.game_name, args.num_players, args.num_random_bots, args.num_simulations)