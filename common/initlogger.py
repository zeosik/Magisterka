import logging

def initloggerconfiguration(log_level):
    FORMAT = '%(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=log_level, format=FORMAT)

