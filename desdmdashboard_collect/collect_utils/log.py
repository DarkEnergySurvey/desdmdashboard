'''
'''

import logging


def get_logger(name):

    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(name)

    handler = logging.FileHandler('desdmdashboard_collect.log')
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter("[ %(asctime)s ] [ %(levelname)s ] [ %(module)s ] : %(message)s",
                              "%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
