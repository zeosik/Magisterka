import logging

from common.initlogger import initloggerconfiguration
from simulator import simulatorengine

if __name__ == "__main__":
    initloggerconfiguration()

    simulatorengine.run()