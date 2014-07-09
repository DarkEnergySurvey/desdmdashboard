'''
'''

import os
import logging

LOG_DIR = os.environ['COLLECT_LOG_DIR']
LOG_FILE = os.environ['COLLECT_LOG_FILE']

loggers = {}

def get_logger(name):
    global loggers

    if name in loggers:
        return loggers.get(name)

    else:
        logging.basicConfig(level=logging.DEBUG)
        logger = logging.getLogger(name)
        desdash_logfile_path = os.path.normpath(LOG_DIR)
        if not os.path.exists(desdash_logfile_path):
            os.makedirs(desdash_logfile_path)
        logfile = os.path.join(desdash_logfile_path, LOG_FILE)

        handler = logging.FileHandler(logfile)
        handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
                "[ %(asctime)s ] [ %(levelname)s ] [ %(module)s ] : %(message)s",
	    		"%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        loggers[name] = logger

	return logger
