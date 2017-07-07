import logging

from simulator import simulatorengine

if __name__ == "__main__":
    FORMAT = '%(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)

    simulatorengine.run()