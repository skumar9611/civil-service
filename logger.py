"""Logger script

A script to log custom message, info, debug and errors occurring in the application.

"""

import logging
import os
from logging.handlers import TimedRotatingFileHandler

from config import config


def get_logger():
    """
    Method to initiate the logging for the application
    :return: logger object
    """
    try:
        log = logging.getLogger('app')
        if not log.handlers:
            log_handler = TimedRotatingFileHandler(os.path.join(os.getcwd(), config['log_file']), when='D', interval=7,
                                                   backupCount=5, encoding=None, delay=False, utc=False)
            formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
            log_handler.setFormatter(formatter)
            log.addHandler(log_handler)
            log.setLevel(logging.DEBUG)
            log.propagate = False

        return log
    except Exception as e:
        return e


logger = get_logger()
