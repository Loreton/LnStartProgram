#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
# updated by Loreto: 19-10-2017 16.00.27
# -----------------------------------------------
from    sys import exit as sysExit
import  logging, time
from    pathlib import Path
import  inspect

myLOGGER = None



# =============================================
# = Logging
#   %(pathname)s    Full pathname of the source file where the logging call was issued(if available).
#   %(filename)s    Filename portion of pathname.
#   %(module)s      Module (name portion of filename).
#   %(funcName)s    Name of function containing the logging call.
#   %(lineno)d      Source line number where the logging call was issued (if available).
# =============================================
def InitLogger(fFILE=None, fCONSOLE=False, ARGS=None):
    global myLOGGER

    if not fFILE and not fCONSOLE:
        myLOGGER = None
        return _setNullLogger()

        # ------------------
        # set up Logger
        # %(levelname)-5.5s limita a 5 prendendo MAX 5 chars
        # logFormatter = logging.Formatter("%(asctime)s - [%(name)-20.20s:%(lineno)4d] - %(levelname)-5.5s - %(message)s", datefmt='%H:%M:%S')
        # logFormatter = logging.Formatter('[%(asctime)s] [%(module)s:%(funcName)s:%(lineno)d] %(levelname)-5.5s - %(message)s','%m-%d %H:%M:%S')
        # ------------------
    logFormatter = logging.Formatter('[%(asctime)s] [%(filename)s:%(lineno)d] %(levelname)-5.5s - %(message)s','%m-%d %H:%M:%S')
    logger       = logging.getLogger()
    logger.setLevel(logging.DEBUG)

        # log to file
    if fFILE:
        ''' impostalo manualmente
            LOG_DIR = Path(fFILE)
            LOG_DIR.mkdir(parents=True, exist_ok=True) # se esiste non dare errore
            LOG_FILE_NAME = LOG_DIR.joinpath('LnStartProgra_' + time.strftime('%Y-%m-%d') + '.log')
        '''
        LOG_FILE_NAME = fFILE
        LOG_DIR = Path(fFILE).parent
        LOG_DIR.mkdir(parents=True, exist_ok=True) # se esiste non dare errore

        print ('using log file:', LOG_FILE_NAME)

        fileHandler = logging.FileHandler('{0}'.format(LOG_FILE_NAME))
        fileHandler.setFormatter(logFormatter)
        logger.addHandler(fileHandler)

        # log to the console
    if fCONSOLE:
        consoleFormatter = logFormatter
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(consoleFormatter)
        logger.addHandler(consoleHandler)



    logger.info('\n'*3)

        # - logging dei parametri di input
    if ARGS:
        logger.info("--------- input ARGS ------- ")
        for key, val in ARGS.items():
            logger.info("{KEY:<20} : {VAL}".format(KEY=key, VAL=val))
        logger.info('--------------------------- ')

    myLOGGER = logger
    return logger




##############################################################################
# - logger dummy
##############################################################################
def _setNullLogger(package=None):


        ##############################################################################
        # - classe che mi permette di lavorare nel caso il logger non sia richiesto
        ##############################################################################
    class nullLogger():
        def __init__(self, package=None, stackNum=1):
            pass


        def info(self, data):
            pass
            # self._print(data)

        def debug(self, data):
            pass
            # self._print(data)

        def error(self, data):  pass
        def warning(self, data):  pass


        def _print(self, data, stackNum=2):
            TAB = 4
            data = '{0}{1}'.format(TAB*' ',data)
            caller = inspect.stack()[stackNum]
            dummy, programFile, lineNumber, funcName, lineCode, rest = caller
            if funcName == '<module>': funcName = '__main__'
            str = "[{FUNC:<20}:{LINENO}] - {DATA}".format(FUNC=funcName, LINENO=lineNumber, DATA=data)
            print (str)

    return nullLogger()


# ====================================================================================
# richiamando questa funzione posso dirottare l'out della log su CONSOLE previa
# impostazione del logger.ini con:
# ====================================================================================
def SetLogger(package, stackNum=0):
    stackLevel = stackNum+1
    if myLOGGER:
        logger = logging.getLogger(package)
        logger.debug('......called by:{CALLER}'.format(CALLER=_GetCaller(stackLevel+2)))
        return logger
    else:
        return _setNullLogger()


###############################################
#
###############################################
def _GetCaller(deepLevel=0, funcName=None):
    try:
        caller  = inspect.stack()[deepLevel]
    except Exception as why:
        return '{0}'.format(why)   # potrebbe essere out of stack ma ritorniamo comunque la stringa

    # print ('..........caller', caller)
    programFile = caller[1]
    lineNumber  = caller[2]
    if not funcName: funcName = caller[3]
    lineCode    = caller[4]
    fname       = (Path(programFile).name).split('.')[0]

    if funcName == '<module>':
        data = "[{0}:{1}]".format(fname, lineNumber)
    else:
        data = "[{0}:{1}]".format(fname, lineNumber)
        # data = "[{0}.{1}:{2}]".format(fname, funcName, lineNumber)

    return data
