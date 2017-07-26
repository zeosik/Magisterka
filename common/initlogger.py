import logging


def initloggerconfiguration(debug: bool):
    FORMAT = '%(name)s - %(levelname)s - %(message)s'
    if debug:
        logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    else:
        logging.basicConfig(level=logging.INFO, format=FORMAT)

