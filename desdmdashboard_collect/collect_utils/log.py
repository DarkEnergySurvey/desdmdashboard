'''
'''

import os
import logging

loggers = {}


def get_logger(name):
    global loggers

    if name in loggers:
        return loggers.get(name)

    else:
	logging.basicConfig(level=logging.DEBUG)
	logger = logging.getLogger(name)

        logfile = 'desdmdashboard_collect.log'
	desdash_logfile_path = os.path.normpath('/desdmdashboard_collect/log/')
        if os.path.exists(desdash_logfile_path):
	    logfile = os.path.join(desdash_logfile_path, logfile)
	handler = logging.FileHandler(logfile)
	handler.setLevel(logging.DEBUG)

	formatter = logging.Formatter("[ %(asctime)s ] [ %(levelname)s ] [ %(module)s ] : %(message)s",
	    		      "%Y-%m-%d %H:%M:%S")
	handler.setFormatter(formatter)
	logger.addHandler(handler)

        loggers[name] = logger

	return logger
