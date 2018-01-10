#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
#
# updated by ...: Loreto Notarantonio
# Version ......: 10-01-2018 15.33.46
# -----------------------------------------------

'''
purtroppo una volta impostato il nome
'''
import  sys, os
import  logging
# from logging.handlers import RotatingFileHandler
from    pathlib import Path
import  inspect

myLOGGER   = None
myLogLevel = logging.INFO
fDEBUG     = False

class LnClass(): pass


# modulesToLog = []



   # if printStack:
   #      logWrite("EXIT STACK:")
   #      print()
   #      for i in reversed(list(range(1, stackLevel))):
   #          caller = _calledBy(i)
   #          if not 'index out of range' in caller:
   #              logWrite("    {0}".format(caller))
   #              if console:
   #                  C.printColored(color=printColor, text=caller, tab=8)
   #  sys.exit(rcode)


# http://stackoverflow.com/questions/16203908/how-to-input-variables-in-logger-formatter
class ContextFilter(logging.Filter):
    """
    This is a filter which injects contextual information into the log.

    Rather than use actual contextual information, we just use random
    data in this demo.
    """
    def __init__(self, defaultStack=5):
        self._defaultStack  = defaultStack
        self._line          = None
        self._LnFuncName    = None      # creata da me
        self._stack         = defaultStack
        '''
        ho verificato che con 5 sembra andare bene
        usato quando chiamato direttamete dal logger
        quando lo chiamo dal SetLogger devo impostaro a 6
        '''

    def setLineNO(self, number):
        self._line = number

    def setFuncName(self, name):
        self._LnFuncName = name

    def setStack(self, number):
        self._stack = number if number else self._defaultStack

    def filter(self, record):
        # print (record)
        if self._line:
            record.lineno = self._line
        else:
            record.lineno = sys._getframe(self._stack).f_lineno

        if self._LnFuncName:
            record.LnFuncName  = self._LnFuncName
        else:
            record.LnFuncName  = sys._getframe(self._stack).f_code.co_name

        return True



###########################################################
# permette di iniettare campi custom nel log-Record
# il problema di questa routine è che se imposto il nome
# di una funzione chiamata, mi rimane valido ache all'uscita
# finché qualcun altro non resetta tale nome con un'altra setLogger()...
###########################################################
def setMyLogRecord(myFuncName='nameNotPassed', lineNO=0):
    if fDEBUG:
        print ('setting funcName to:', myFuncName)

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

    global myLOGGER, LnFilter

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

    ''' --- con myLogRecord
    '''
    fileFMT    = '[%(asctime)s] [%(LnFuncName)-20s:%(lineno)4d] %(levelname)-5.5s - %(message)s'
    consoleFMT = '[%(LnFuncName)-20s:%(lineno)4d] %(levelname)-5.5s - %(message)s'


    logger = logging.getLogger()

    # - inserimento contextFilter
    LnFilter    = ContextFilter()
    logger.addFilter(LnFilter)
    logger.setLevel(myLogLevel)

    # setMyLogRecord('Ln-Initialize')


        # log to file
    if _fFILE:
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
def SetLogger(package, stackNum=0, reset=False):
    global fDEBUG
    fDEBUG = False
    if fDEBUG:
        print ('...')
        print (package)

    if not myLOGGER:
        return _setNullLogger()

    CALLER = []
    for stacklevel in [0,1,2,3]:
        caller = _GetCaller(stacklevel)
        CALLER.append(caller)

    if fDEBUG:
        TAB= ' '*4
        for stacklevel in [0,1,2,3]:
            print('stacklevel..:', stacklevel)
            caller = CALLER[stacklevel]
            for key, val in caller0.items():
                print (TAB, '{:<15}: {}'.format(key, val))
            print()



        # ---------------------------------
        # - individuiamo se è un modulo
        # - da tracciare o meno
        # ---------------------------------
    fullPkg = (package + '.' + CALLER[1]._funcname)
    if '!ALL!' in modulesToLog:
        LOG_LEVEL = myLogLevel

    else:
        fullPkg_LOW = fullPkg.lower()
        LOG_LEVEL = None
        for moduleStr in modulesToLog:
            if moduleStr.lower() in fullPkg_LOW:
                LOG_LEVEL = myLogLevel


    if fDEBUG:
        print ('fullPkg   :', fullPkg )
        print ('LOG_LEVEL :', LOG_LEVEL )


    if not LOG_LEVEL:
        logger = _setNullLogger()
        return logger


    logger = logging.getLogger(package)
    logger.setLevel(LOG_LEVEL)

        # --------------------------------------------------
        # - aggiungiamo il ContextFilter
        # - IMPORTANTE in quanto quello inserito nel init
        # - contiene i valori di default usati quando
        # - chiamato dall logger.xxx()
        # --------------------------------------------------
    logger.addFilter(LnFilter)
    LnFilter.setStack(6)    # cambio lo stackNum

    if reset:
        logger.info('.... exiting\n')
        LnFilter.setStack(None)    # cambio lo stackNum
        return


    logger.info('.... entering called by: {CALLER}'.format(CALLER=CALLER[3]._fullcaller))
    LnFilter.setStack(None)    # cambio lo stackNum

    if fDEBUG:
        print ('...\n')

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





###############################################
#
###############################################
def _GetCaller(stackLevel=0):
    retCaller = LnClass()

    try:
        dummy, programFile, lineNumber, funcName, lineCode, rest = inspect.stack()[stackLevel]

    except Exception as why:
        retCaller._fullcaller  = str(why)
        return myCaller   # potrebbe essere out of stack ma ritorniamo comunque la stringa


    if funcName == '<module>': funcName = '__main__'

    retCaller._funcname   = funcName
    retCaller._linecode   = lineCode
    retCaller._lineno     = lineNumber
    retCaller._fullfname  = programFile

    fname                   = os.path.basename(programFile).split('.')[0]
    retCaller._fname      = fname
    retCaller._fullcaller = "[{0}.{1}:{2}]".format(fname, funcName, lineNumber)

    return retCaller
