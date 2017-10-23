#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
# updated by Loreto: 23-10-2017 17.56.54
# -----------------------------------------------
from    sys import exit as sysExit, _getframe as getframe
import  logging, time
from    pathlib import Path
import  inspect

myLOGGER    = None
toFILE      = []
toCONSOLE   = []
modulesToLog = []


# =============================================
# = Logging
#   %(pathname)s    Full pathname of the source file where the logging call was issued(if available).
#   %(filename)s    Filename portion of pathname.
#   %(module)s      Module (name portion of filename).
#   %(funcName)s    Name of function containing the logging call.
#   %(lineno)d      Source line number where the logging call was issued (if available).
# =============================================
def InitLogger(fFILE=None, fCONSOLE=False, ARGS=None):
    global myLOGGER, toFILE, toCONSOLE, modulesToLog

    if not fFILE and not fCONSOLE:
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
    if fFILE:
        toFILE = True
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
        toCONSOLE = fCONSOLE
        modulesToLog = fCONSOLE
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


# ====================================================================================
# - dal package passato come parametro cerchiamo di individuare se la fuzione/modulo
# - è tra quelli da fare il log.
# -
# ====================================================================================
def SetLogger(package, stackNum=0):
    if not myLOGGER:
        return _setNullLogger()


    stackLevel = stackNum + 1                 # aggiungiamo quello richiesto dal caller
    print (stackLevel)
    funcName    = getframe(stackLevel).f_code.co_name
    if funcName == '<module>': funcName = '__main__'


        # - tracciamo la singola funzione oppure modulo oppure libreria od altro
    if modulesToLog:
        LOG_LEVEL = None # default
        fullPkg = (package + funcName).lower()
        print (fullPkg)
        for moduleStr in modulesToLog:
            if moduleStr.lower() in fullPkg:
                LOG_LEVEL = logging.DEBUG

    else:
        LOG_LEVEL = logging.DEBUG


    logger = logging.getLogger(package)

    if LOG_LEVEL:
        logger.setLevel(LOG_LEVEL)
    else:
        logger = _setNullLogger()

    logger.debug('......called by:{CALLER}'.format(CALLER=_GetCaller(stackLevel+1)))
    return logger



    # -----------------------------------------------------------------------------------------
    # - Per quanto riguarda il setLogger, devo intervenire sul numero di riga della funzione
    # - altrimenti scriverebbe quello della presente funzione.
    # - Per fare questo utilizzo l'aggiunta di un filtro passandogli il lineNO corretto
    # - per poi ripristinarlo al default
    # -----------------------------------------------------------------------------------------

    # print ('..........', LOG_LEVEL, pkgName)


         # logger.setLevel(logging.NOTSET)  # oppure FATAL

        # - creiamo il contextFilter
    LnFilter    = _ContextFilter()

        # - aggiungiamolo al logger attuale
    logger.addFilter(LnFilter)

        # - modifichiamo la riga della funzione chiamante
    LnFilter.setLineNO(funcLineNO)

        # ----------------------------------------------------------------------------------
        # - inseriamo la riga con riferimento al chiamante di questa fuznione
        # - nel "...called by" inseriamo il caller-1
        # ----------------------------------------------------------------------------------
    # logger.debug('')

        # --------------------------------------------------------------------------
        # - azzeriamo il lineNO in modo che le prossime chiamate al logger, che
        # - non passano da questa funzione, prendano il lineNO corretto.
        # --------------------------------------------------------------------------
    LnFilter.setLineNO(None)
    LnFilter.setStack(5)            # ho verificato che con 5 sembra andare bene

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
