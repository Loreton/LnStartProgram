#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
# updated by Loreto: 24-10-2017 09.10.33
# -----------------------------------------------
from    sys import exit as sysExit, _getframe as getframe
import  logging, time
from    pathlib import Path
import  inspect

myLOGGER    = None
modulesToLog = []


# =============================================
# = Logging
#   %(pathname)s    Full pathname of the source file where the logging call was issued(if available).
#   %(filename)s    Filename portion of pathname.
#   %(module)s      Module (name portion of filename).
#   %(funcName)s    Name of function containing the logging call.
#   %(lineno)d      Source line number where the logging call was issued (if available).
# =============================================
def init(toFILE=None, toCONSOLE=False, logfilename=None, ARGS=None):
    global myLOGGER, modulesToLog



        # ----------------------------------------------------------------
        # - impostazione relativamente complessa ai moduli...
        # - toCONSOLE & toFILE  non dovrebbero mai essere contemporanei
        # - perché bloccati dal ParseInput
        # ----------------------------------------------------------------
    if toFILE:
        modulesToLog = toFILE

    elif toCONSOLE:
        modulesToLog = toCONSOLE

    elif toCONSOLE == [] or toFILE == []:
        modulesToLog = ['!ALL!']

    else:
        modulesToLog = False


    print(__file__, 'modulesToLog..................', modulesToLog)


    if not toFILE and not toCONSOLE:
        myLOGGER = None
        return _setNullLogger()

        # ------------------
        # set up Logger
        # %(levelname)-5.5s limita a 5 prendendo MAX 5 chars
        # logFormatter = logging.Formatter("%(asctime)s - [%(name)-20.20s:%(lineno)4d] - %(levelname)-5.5s - %(message)s", datefmt='%H:%M:%S')
        # logFormatter = logging.Formatter('[%(asctime)s] [%(module)s:%(funcName)s:%(lineno)d] %(levelname)-5.5s - %(message)s','%m-%d %H:%M:%S')
        # ------------------
    # logFormatter = logging.Formatter('[%(asctime)s] [%(name)-25s:%(lineno)4d] %(levelname)-5.5s - %(message)s','%m-%d %H:%M:%S')
    logFormatter = logging.Formatter('[%(asctime)s] [%(module)-25s:%(lineno)4d] %(levelname)-5.5s - %(message)s','%m-%d %H:%M:%S')
    logFormatter = logging.Formatter('[%(asctime)s] [%(module)s:%(lineno)4d] %(levelname)-5.5s - %(message)s','%m-%d %H:%M:%S')
    logger       = logging.getLogger()
    logger.setLevel(logging.DEBUG)
        # log to file
    if toFILE:
        LOG_FILE_NAME = logfilename
        LOG_DIR = Path(logfilename).parent
        LOG_DIR.mkdir(parents=True, exist_ok=True) # se esiste non dare errore

        print ('using log file:', LOG_FILE_NAME)

        fileHandler = logging.FileHandler('{0}'.format(LOG_FILE_NAME))
        fileHandler.setFormatter(logFormatter)
        logger.addHandler(fileHandler)

        # log to the console
    if toCONSOLE:
        consoleFormatter = logFormatter
        consoleHandler   = logging.StreamHandler()
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
# InitLogger = init

# ====================================================================================
# - dal package passato come parametro cerchiamo di individuare se la fuzione/modulo
# - è tra quelli da fare il log.
# - Il package mi server per verficare se devo loggare il modulo o meno
# ====================================================================================
def SetLogger(package, stackNum=0):
    if not myLOGGER:
        return _setNullLogger()

    # print ('..................', modulesToLog)

    stackLevel = stackNum + 1                 # aggiungiamo quello richiesto dal caller
    # print (stackLevel)
    funcName    = getframe(stackLevel).f_code.co_name
    if funcName == '<module>': funcName = '__main__'


        # - tracciamo la singola funzione oppure modulo oppure libreria od altro
    if modulesToLog == False:
        LOG_LEVEL = None

    elif '!ALL!' in modulesToLog:
        LOG_LEVEL = logging.DEBUG

    elif modulesToLog:
        LOG_LEVEL = None # default
        fullPkg = (package + funcName).lower()
        for moduleStr in modulesToLog:
            if moduleStr.lower() in fullPkg:
                LOG_LEVEL = logging.DEBUG



    print(__file__, 'LOG_LEVEL..................', LOG_LEVEL)

    logger = logging.getLogger(package)

    if LOG_LEVEL:
        logger.setLevel(LOG_LEVEL)
    else:
        logger = _setNullLogger()

    logger.debug('......called by:{CALLER}'.format(CALLER=_GetCaller(stackLevel+1)))
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



# http://stackoverflow.com/questions/16203908/how-to-input-variables-in-logger-formatter
class _ContextFilter(logging.Filter):
    """
    This is a filter which injects contextual information into the log.
    """
    def __init__(self):
        self._line  = None
        self._stack = 5    # default

    def setLineNO(self, number):
        self._line = number

    def setStack(self, number):
        self._stack = number

    def filter(self, record):
        if self._line:
            record.lineno = self._line
        else:
            # record.name   = getframe(stack).f_code.co_name
            record.lineno = getframe(self._stack).f_lineno
        return True
