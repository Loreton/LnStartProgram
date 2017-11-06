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
fDEBUG    = False
modulesToLog = []


# =============================================
# = Logging
#   %(pathname)s    Full pathname of the source file where the logging call was issued(if available).
#   %(filename)s    Filename portion of pathname.
#   %(module)s      Module (name portion of filename).
#   %(funcName)s    Name of function containing the logging call.
#   %(lineno)d      Source line number where the logging call was issued (if available).
# =============================================
def init(toFILE=False, toCONSOLE=False, logfilename=None, ARGS=None):
    global myLOGGER, modulesToLog, fDEBUG


    if ARGS:
        if 'debug' in ARGS:
            fDEBUG = ARGS['debug']


        # ----------------------------------------------------------------
        # - impostazione relativamente complessa ai moduli...
        # - toCONSOLE & toFILE  non dovrebbero mai essere contemporanei
        # - perché bloccati dal ParseInput
        # - toCONSOLE==[] significa tutti i moduli
        # ----------------------------------------------------------------
    if toCONSOLE==[]:
        modulesToLog = ['!ALL!']
        toCONSOLE = True

    elif toCONSOLE:
        modulesToLog = toCONSOLE # copy before modifying it
        toCONSOLE = True

    elif toFILE==[]:
        modulesToLog = ['!ALL!']
        toFILE = True

    elif toFILE:
        modulesToLog = toFILE   # copy before modifying it
        toFILE = True

    else:
        # modulesToLog = []
        myLOGGER = None
        if fDEBUG: print(__name__, 'no logger has been activated')
        return _setNullLogger()

    if fDEBUG: print(__name__, 'modulesToLog..................', modulesToLog)


        # ------------------
        # set up Logger
        # %(levelname)-5.5s limita a 5 prendendo MAX 5 chars
        # logFormatter = logging.Formatter("%(asctime)s - [%(name)-20.20s:%(lineno)4d] - %(levelname)-5.5s - %(message)s", datefmt='%H:%M:%S')
        # logFormatter = logging.Formatter('[%(asctime)s] [%(module)s:%(funcName)s:%(lineno)d] %(levelname)-5.5s - %(message)s','%m-%d %H:%M:%S')
        # ------------------
    # logFormatter = logging.Formatter('[%(asctime)s] [%(name)-25s:%(lineno)4d] %(levelname)-5.5s - %(message)s','%m-%d %H:%M:%S')
    logFormatter = logging.Formatter('[%(asctime)s] [%(module)-25s:%(lineno)4d] %(levelname)-5.5s - %(message)s','%m-%d %H:%M:%S')
    # logFormatter = logging.Formatter('[%(asctime)s] [%(module)s:%(lineno)4d] %(levelname)-5.5s - %(message)s','%m-%d %H:%M:%S')
    logger       = logging.getLogger()
    logger.setLevel(logging.DEBUG)
        # log to file
    if toFILE:
        LOG_FILE_NAME = logfilename
        LOG_DIR = Path(logfilename).parent
        LOG_DIR.mkdir(parents=True, exist_ok=True) # se esiste non dare errore

        if fDEBUG: print ('using log file:', LOG_FILE_NAME)

        fileHandler = logging.FileHandler('{0}'.format(LOG_FILE_NAME))
        fileHandler.setFormatter(logFormatter)
        logger.addHandler(fileHandler)

        # log to the console
    if toCONSOLE:
        # consoleFormatter = logFormatter
        consoleFormatter = logging.Formatter('[%(module)-25s:%(lineno)4d] %(levelname)-5.5s - %(message)s','%m-%d %H:%M:%S')
        consoleHandler   = logging.StreamHandler()
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
# InitLogger = init

# ====================================================================================
# - dal package passato come parametro cerchiamo di individuare se la fuzione/modulo
# - è tra quelli da fare il log.
# - Il package mi server per verficare se devo loggare il modulo o meno
# ====================================================================================
def SetLogger(package, stackNum=0):
    if not myLOGGER:
        return _setNullLogger()

    funcName        = getframe(stackNum + 1).f_code.co_name
    funcName_prev    = getframe(stackNum).f_code.co_name

    if funcName == '<module>': funcName = '__main__'


        # - tracciamo la singola funzione oppure modulo oppure libreria od altro

    if '!ALL!' in modulesToLog:
        LOG_LEVEL = logging.DEBUG

    else:
        LOG_LEVEL = None # default
        fullPkg = (package + funcName).lower()
        for moduleStr in modulesToLog:
            if moduleStr.lower() in fullPkg:
                LOG_LEVEL = logging.DEBUG


    if False:
        print(__name__, 'package..................', package)
        print(__name__, 'funcName.................', funcName)
        print(__name__, 'funcName_prev............', funcName_prev)
        print(__name__, 'LOG_LEVEL................', LOG_LEVEL)
        print()


    if LOG_LEVEL:
        logger = logging.getLogger(package)
        logger.setLevel(LOG_LEVEL)
        # caller = inspect.stack()[stackNum]
        # dummy, programFile, lineNumber, funcName, lineCode, rest = caller
        logger.info('\n')
        logger.info('{TARGET}......called by:{CALLER}'.format(TARGET=funcName_prev, CALLER=_GetCaller(stackNum+2)))

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
# Ho scoperto che potrei anche usare la call seguente
# ma non avrei il controllo sullo stackNO.
#   fn, lno, func, sinfo = myLOGGER.findCaller(stack_info=False)
#   print (fn, lno, func, sinfo)
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
        # data = "[{0}:{1}]".format(fname, lineNumber)
        data = "[{0}:{1}]".format(funcName, lineNumber)
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


'''
    def findCaller(self, stack_info=False):
        """
        Find the stack frame of the caller so that we can note the source
        file name, line number and function name.
        """
        f = currentframe()
        #On some versions of IronPython, currentframe() returns None if
        #IronPython isn't run with -X:Frames.
        if f is not None:
            f = f.f_back
        rv = "(unknown file)", 0, "(unknown function)", None
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            if filename == _srcfile:
                f = f.f_back
                continue
            sinfo = None
            if stack_info:
                sio = io.StringIO()
                sio.write('Stack (most recent call last):\n')
                traceback.print_stack(f, file=sio)
                sinfo = sio.getvalue()
                if sinfo[-1] == '\n':
                    sinfo = sinfo[:-1]
                sio.close()
            rv = (co.co_filename, f.f_lineno, co.co_name, sinfo)
            break
        return rv
'''