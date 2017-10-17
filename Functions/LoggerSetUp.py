#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
# updated by Loreto: 16-10-2017 17.04.47
# -----------------------------------------------
import os
import logging, time

# =============================================
# = Logging
# =============================================
def LoggerSetUp(CONSOLE=False):
    LOG_DIR = 'log'
    LOG_FILE_NAME = 'pyd3_' + time.strftime('%Y-%m-%d_%H-%M-%S') + '.log'

    # set up Logger
    #   %(pathname)s    Full pathname of the source file where the logging call was issued(if available).
    #   %(filename)s    Filename portion of pathname.
    #   %(module)s      Module (name portion of filename).
    #   %(funcName)s    Name of function containing the logging call.
    #   %(lineno)d      Source line number where the logging call was issued (if available).
    logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s] %(message)s", datefmt='%Y-%m-%d %H:%M:%S')
    logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s] %(message)s", datefmt='%H:%M:%S')
    logFormatter = logging.Formatter("%(asctime)s - [%(name)-20.20s:%(lineno)4d] - %(levelname)-5.5s - %(message)s", datefmt='%H:%M:%S')
    logFormatter = logging.Formatter('[%(asctime)s] [%(module)s:%(funcName)s:%(lineno)d] %(levelname)-5.5s - %(message)s','%m-%d %H:%M:%S')
    logFormatter = logging.Formatter('[%(asctime)s] [%(filename)s:%(lineno)d] %(levelname)-5.5s - %(message)s','%m-%d %H:%M:%S')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

        # log to the console
    if CONSOLE:
        # %(levelname)-5.5s limita a 5 prendendo MAX 5 chars
        consoleFormatter = logging.Formatter("%(asctime)s - [%(name)-20.20s:%(lineno)4d] - %(levelname)-5.5s - %(message)s", datefmt='%H:%M:%S')
        consoleFormatter = logging.Formatter('[%(asctime)s] [%(module)s:%(funcName)s:%(lineno)d] %(levelname)-5.5s - %(message)s','%m-%d %H:%M:%S')
        consoleFormatter = logFormatter
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(consoleFormatter)
        logger.addHandler(consoleHandler)

        # also log to a file
    if not os.path.exists(LOG_DIR):
        logger.info("Creating log directory: {}".format(LOG_DIR))
        os.makedirs(LOG_DIR)
    fileHandler = logging.FileHandler('{0}/{1}'.format(LOG_DIR, LOG_FILE_NAME))
    fileHandler.setFormatter(logFormatter)
    logger.addHandler(fileHandler)

    return logger


