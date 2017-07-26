import logging, argparse

from common.initlogger import initloggerconfiguration
from simulator import simulatorengine

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--num_players", help="Ilosc graczy", type=int, default=3)
    parser.add_argument("-f", "--num_humans", help="Ilosc fizycznych graczy", type=int, default=0)
    parser.add_argument("-d", "--debug", help="Wypisz informacje debugowe", action='store_true')
    args = parser.parse_args()

    initloggerconfiguration(args.debug)

    simulatorengine.run(args.num_players, args.num_humans)