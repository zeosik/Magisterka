import logging

from simulator import simulatorengine

if __name__ == "__main__":
    FORMAT = '%(asctime)-15s - %(threadName)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)

    simulatorengine.run()