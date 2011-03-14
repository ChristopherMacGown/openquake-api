# -*- coding: utf-8 -*-
"""
Set up some system-wide loggers
TODO(jmc): init_logs should take filename, or sysout
TODO(jmc): support debug level per logger.

"""
import logging
import logging.handlers

LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warn': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL,
          # The default logging levels are: CRITICAL=50, ERROR=40, WARNING=30,
          # INFO=20, DEBUG=10, NOTSET=0
          # The 'validate' log level is defined here as 25 because it is 
          # considered to be less critical than a WARNING but slightly more
          # critical than INFO.
          'validate': 25}

LOG = logging.getLogger()

def init_logs(level):
    """Load logging config, and set log levels based on flags"""
    
    level = LEVELS.get(level, logging.ERROR)
    logging.basicConfig(level=level)
    logging.getLogger("").setLevel(logging.ERROR)
    LOG.addHandler(logging.handlers.RotatingFileHandler('test', 
                                                        backupCount=5))
    
    LOG.setLevel(level)
