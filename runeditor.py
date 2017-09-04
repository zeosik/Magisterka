from common.initlogger import initloggerconfiguration
from editor import window
import logging

if __name__ == "__main__":
    initloggerconfiguration(logging.DEBUG)
    window.run()