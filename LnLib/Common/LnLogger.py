#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
#
# updated by ...: Loreto Notarantonio
# Version ......: 02-01-2018 11.53.45
# -----------------------------------------------
import  sys
import  logging
# from logging.handlers import RotatingFileHandler
from    pathlib import Path
import  inspect

myLOGGER   = None
myLogLevel = logging.INFO
fDEBUG     = False
# modulesToLog = []



###########################################################
# permette di iniettare campi custom nel log-Record
###########################################################
def setMyLogRecord(myFuncName='nameNotPassed', lineNO=0):
    old_factory = logging.getLogRecordFactory()
    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        record.LnFuncName = myFuncName
        # record.LnLineNO   = lineNO   # non posso altrimenti rimane sempre lo stesso
        return record
    logging.setLogRecordFactory(record_factory)


from logging.handlers import RotatingFileHandler

#----------------------------------------------------------------------
def create_rotating_log(path):
    """
    Creates a rotating log
    """
    logger = logging.getLogger("Rotating Log")
    logger.setLevel(logging.INFO)

    # add a rotating handler
    handler = RotatingFileHandler(path, maxBytes=20, backupCount=5)
    logger.addHandler(handler)



def prepareLogEnv(toFILE=False, toCONSOLE=False, logfilename=None, loglevel='info', ARGS=None):
    ''' ----------------------------------------------------------------
         impostazione relativamente complessa ai moduli...
         toCONSOLE & toFILE  non dovrebbero mai essere contemporanei
         perché bloccati dal ParseInput
         toCONSOLE==[] significa log di tutti i moduli
         toFILE==[]    significa log di tutti i moduli
        ---------------------------------------------------------------- '''
    global modulesToLog, fDEBUG, myLogLevel

    # - SETting LOGLEVEL
    assert type(loglevel) == str
    if loglevel.lower() == 'debug':
        myLogLevel = logging.DEBUG
    elif loglevel.lower() == 'warning':
        myLogLevel = logging.WARNING
    else:
        myLogLevel = logging.INFO


    _fLOG, _fCONSOLE, _fFILE = True, False, False


    if ARGS:
        if 'debug' in ARGS:
            fDEBUG = ARGS['debug']


    if toCONSOLE==[]:
        modulesToLog = ['!ALL!']
        _fCONSOLE = True

    elif toCONSOLE:
        modulesToLog = toCONSOLE # copy before modifying it
        _fCONSOLE = True

    elif toFILE==[]:
        modulesToLog = ['!ALL!']
        _fFILE = True

    elif toFILE:
        modulesToLog = toFILE   # copy before modifying it
        _fFILE = True

    else:
        modulesToLog = []
        _fLOG = False
        if fDEBUG: print(__name__, 'no logger has been activated')

    if fDEBUG:
        print(__name__, 'modulesToLog..................', modulesToLog)

    return _fLOG, _fCONSOLE, _fFILE


# =============================================
# = Logging
#   %(pathname)s    Full pathname of the source file where the logging call was issued(if available).
#   %(filename)s    Filename portion of pathname.
#   %(module)s      Module (name portion of filename).
#   %(funcName)s    Name of function containing the logging call.
#   %(lineno)d      Source line number where the logging call was issued (if available).
# =============================================
def init(   toFILE=False,
            toCONSOLE=False,
            logfilename=None,
            defaultLogLevel='info',
            ARGS=None,
            ROTATE='time',
            backupCount=5,
            maxBytes=20000,
            when="m",
            interval=60,
            ):

    global myLOGGER

    _fLOG, _fCONSOLE, _fFILE = prepareLogEnv(toFILE=toFILE, toCONSOLE=toCONSOLE, logfilename=logfilename, ARGS=ARGS, loglevel=defaultLogLevel)
    if not _fLOG:
        myLOGGER = None
        return _setNullLogger()

        # ------------------
        # set up Logger
        # %(levelname)-5.5s limita a 5 prendendo MAX 5 chars
        # logFormatter = logging.Formatter("%(asctime)s - [%(name)-20.20s:%(lineno)4d] - %(levelname)-5.5s - %(message)s", datefmt='%H:%M:%S')
        # logFormatter = logging.Formatter('[%(asctime)s] [%(module)s:%(funcName)s:%(lineno)d] %(levelname)-5.5s - %(message)s','%m-%d %H:%M:%S')
        # ------------------
    fileFMT    = '[%(asctime)s] [%(LnFuncName)-20s:%(lineno)4d] %(levelname)-5.5s - %(message)s'
    consoleFMT = '[%(LnFuncName)-20s:%(lineno)4d] %(levelname)-5.5s - %(message)s'


    logger = logging.getLogger()
    logger.setLevel(myLogLevel)
    # print (myLogLevel)
    setMyLogRecord('Ln-Initialize')


        # log to file
    if _fFILE:
        # LOG_FILE_NAME = logfilename
        LOG_DIR = Path(logfilename).parent

            # se esiste non dare errore
        try:
            LOG_DIR.mkdir(parents=True)
        except (FileExistsError):
            pass



        if ROTATE == 'time':
            fileHandler = logging.handlers.TimedRotatingFileHandler(str(logfilename),
                                                                when=when,
                                                                interval=interval,
                                                                backupCount=backupCount)
        elif ROTATE == 'size':
            fileHandler = logging.handlers.RotatingFileHandler(str(logfilename), maxBytes=maxBytes, backupCount=backupCount)
        else:
            # fileHandler = logging.FileHandler('{0}'.format(logfilename))
            fileHandler = logging.FileHandler(str(logfilename))

            # add a file handler
        logger.addHandler(fileHandler)

        fileFormatter   = logging.Formatter(fmt=fileFMT, datefmt='%m-%d %H:%M:%S')
        fileHandler.setFormatter(fileFormatter)

        if fDEBUG: print ('using log file:', logfilename)


        # log to the console
    if _fCONSOLE:
        consoleHandler  = logging.StreamHandler(stream=sys.stdout)
        consoleFormatter= logging.Formatter(fmt=consoleFMT, datefmt='%m-%d %H:%M:%S')
        consoleHandler.setFormatter(consoleFormatter)
        logger.addHandler(consoleHandler)


        # - logging dei parametri di input
    logger.info('\n'*3)
    if ARGS:
        logger.info("--------- input ARGS ------- ")
        for key, val in ARGS.items():
            logger.info("{KEY:<20} : {VAL}".format(KEY=key, VAL=val))
        logger.info('--------------------------- ')
    logger.info('\n'*3)

    myLOGGER = logger
    return logger


# ====================================================================================
# - dal package passato come parametro cerchiamo di individuare se la fuzione/modulo
# - è tra quelli da fare il log.
# - Il package mi server per verficare se devo loggare il modulo o meno
# ====================================================================================
def SetLogger(package, stackNum=0):
    if not myLOGGER:
        return _setNullLogger()

    # comoda ... ma non ho il controllo sullo stackNO.
    # fn, lno, func, sinfo = myLOGGER.findCaller(stack_info=False)
    # print (fn, lno, func, sinfo)

    funcName       = sys._getframe(stackNum+1).f_code.co_name
    funcLineNO     = sys._getframe(stackNum+1).f_lineno
    thisFuncName   = sys._getframe(stackNum).f_code.co_name

    if funcName == '<module>': funcName = '__main__'
    caller = '{}.{}({})'.format(package, funcName, funcLineNO)

    _token = package.split('.')
    _LnFuncName = '{FIRST}.{LAST}.{FUNC}'.format(FIRST=_token[0], LAST=_token[-1], FUNC=funcName)

    if len(_LnFuncName) > 19:
        # _LnFuncName = '{LAST}.{FUNC}'.format(LAST=_token[-1], FUNC=funcName)
        _LnFuncName = '{FUNC}'.format(FUNC=funcName)


    if False:
        print(__name__, 'package..................', package)
        print(__name__, 'funcName -2..............', sys._getframe(stackNum-2).f_code.co_name, sys._getframe(stackNum-2).f_lineno)
        print(__name__, 'funcName -1..............', sys._getframe(stackNum-1).f_code.co_name, sys._getframe(stackNum-1).f_lineno)
        print(__name__, 'funcName ................', sys._getframe(stackNum).f_code.co_name, sys._getframe(stackNum).f_lineno)
        print(__name__, 'funcName +1..............', sys._getframe(stackNum+1).f_code.co_name, sys._getframe(stackNum+1).f_lineno)
        print(__name__, 'funcName +2..............', sys._getframe(stackNum+2).f_code.co_name, sys._getframe(stackNum+2).f_lineno)
        try:
            print(__name__, 'funcName +3..............', sys._getframe(stackNum+3).f_code.co_name, sys._getframe(stackNum+3).f_lineno)
        except:
            pass
        print(__name__, 'called by..............', _LnFuncName, funcLineNO)
        print()



        # ---------------------------------
        # - individuiamo se è un modulo
        # - da tracciare o meno
        # ---------------------------------
    if '!ALL!' in modulesToLog:
        LOG_LEVEL = myLogLevel

    else:
        LOG_LEVEL = None
        fullPkg = (package + funcName).lower()
        for moduleStr in modulesToLog:
            if moduleStr.lower() in fullPkg:
                LOG_LEVEL = myLogLevel



    if LOG_LEVEL:
        logger = logging.getLogger(package)
        logger.setLevel(LOG_LEVEL)

        # - set temporaneo dei nomi per scrivere SetLogger come funzione
        setMyLogRecord(myFuncName=thisFuncName)

        logger.info('\n')
        logger.info('......called by: {CALLER}'.format(CALLER=caller))

        # - set nomi del caller
        setMyLogRecord(myFuncName=_LnFuncName)
    else:
        logger = _setNullLogger()

    return logger














##############################################################################
# - logger dummy
##############################################################################
def _setNullLogger(package=None):

        ##############################################################################
        # - classe che mi permette di lavorare nel caso il logger non sia richiesto
        ##############################################################################
    class nullLogger():
        def __init__(self, package=None, stackNum=1): pass
        def info(self, data):       self._dummy(data)
        def debug(self, data):      self._dummy(data)
        def error(self, data):      self._dummy(data)
        def warning(self, data):    self._dummy(data)

        def _dummy(self, data): pass

        def _print(self, data, stackNum=2):
            TAB = 4
            data = '{0}{1}'.format(TAB*' ',data)
            caller = inspect.stack()[stackNum]
            dummy, programFile, lineNumber, funcName, lineCode, rest = caller
            if funcName == '<module>': funcName = '__main__'
            pkg = package.split('.', 1)[1] + '.' +funcName
            str = "[{FUNC:<20}:{LINENO}] - {DATA}".format(FUNC=pkg, LINENO=lineNumber, DATA=data)
            print (str)

    return nullLogger()
