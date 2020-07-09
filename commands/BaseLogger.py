import os
import logging
from logging.handlers import RotatingFileHandler
from .Statics import *

# create format of the log message
logFormatter = logging.Formatter(LOG_FORMAT)

# Get the path of the running script (api command)
appPath = os.path.dirname(os.path.abspath(__file__))

# add subdirectory "log" to the path
logPath = os.path.join(appPath, 'logs')

if not os.path.isdir(logPath):
    os.makedirs(logPath)

# create full logfilename
logFullPathName = os.path.join(logPath, 'ExportIt.log')

# create log handler
logHandler = RotatingFileHandler(logFullPathName, mode='a', maxBytes=200000, backupCount=2, encoding=None, delay=0)
logHandler.setFormatter(logFormatter)
logHandler.setLevel(LOG_LEVEL)

# create logger
logger = logging.getLogger('ExportIt')
logger.setLevel(LOG_LEVEL)

# add logger no logger is available
if not len(logger.handlers):
    logger.addHandler(logHandler)

logger.debug("Logging started")
