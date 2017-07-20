import logging


def initloggerconfiguration():
    FORMAT = '%(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)
