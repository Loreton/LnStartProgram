#!/usr/bin/python -O
# -*- coding: iso-8859-15 -*-
# -O Optimize e non scrive il __debug__
#
# -----------------------------------------------
__author__  = 'Loreto Notarantonio'
__version__ = 'LnVer_2017-03-30_09.38.23'
# -----------------------------------------------

# ####################################################################################################################

# http://stackoverflow.com/questions/13649664/how-to-use-logging-with-pythons-fileconfig-and-configure-the-logfile-filename
import sys, os
import logging
import logging.config # obbligatorio altrimenti da' l'errore: <'module' object has no attribute 'config'>
import inspect

gPackageQualifiers = 0
isLoggerActive = False   # variabile globale accessibile anche dall'esterno

_logMODULE  = False
_logCONSOLE = False
_LOGGER     = False


# http://stackoverflow.com/questions/16203908/how-to-input-variables-in-logger-formatter
class ContextFilter(logging.Filter):
    """
    This is a filter which injects contextual information into the log.

    Rather than use actual contextual information, we just use random
    data in this demo.
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
            # record.name   = sys._getframe(stack).f_code.co_name
            record.lineno = sys._getframe(self._stack).f_lineno
        return True



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
    if not funcName:
        funcName    = caller[3]
    lineCode    = caller[4]
    fname       = os.path.basename(programFile).split('.')[0]

    if funcName == '<module>':
        data = "[{0}:{1}]".format(fname, lineNumber)
    else:
        data = "[{0}.{1}:{2}]".format(fname, funcName, lineNumber)
    return data



    # ========================================================
    # - INIT del log. Chiamato solo dal MAIN program
    # ========================================================
def InitLogger(iniLogFile, logFileName, package, LOGGER=False, logCONSOLE=False, logMODULE=False, packageQualifiers=2):
    global gPackageQualifiers
    global _logMODULE, _logCONSOLE, _LOGGER

    '''
    if logCONSOLE:
        _LOGGER     = True
        _logCONSOLE = True
        _logMODULE  = logCONSOLE[:]

    elif LogMODULE:
        _LOGGER     = True
        _logCONSOLE = False
        _logMODULE  = LogMODULE[:]

    else:
        _logMODULE  = False
        _logCONSOLE = False
        _LOGGER     = False
    '''

    _logMODULE  = logMODULE
    _logCONSOLE = logCONSOLE
    _LOGGER     = LOGGER


    # print( _LOGGER)


    gPackageQualifiers = packageQualifiers

    if not os.path.isfile(iniLogFile):
        print (iniLogFile, "... NOT FOUND")
        sys.exit()

    logging.config.fileConfig(iniLogFile, disable_existing_loggers=False, defaults={'rotateLogFile': logFileName})
    logger      = logging.getLogger(package)
    LnFilter    = ContextFilter()
    logger.addFilter(LnFilter)

    savedLevel  = logger.getEffectiveLevel()

    logger.setLevel(logging.INFO)
    for i in range(1,10):   logger.info(' ')
    for i in range(1,5):    logger.info('-'*40 + 'Start LOGging' + '-'*20)
    logger.setLevel(savedLevel)

    logFileName = logging.getLoggerClass().root.handlers[0].baseFilename
    # print ("    {0:<32}: {1}".format('LOG file', logFileName))

    return logFileName


def SetNullLogger(package=None):
    global isLoggerActive

    ##############################################################################
    # - classe che mi permette di lavorare nel caso il logger non sia richiesto
    ##############################################################################

    class nullLogger():
            def __init__(self, package=None, stackNum=1):
                '''
                TAB = 0
                self._loggerStackNum = stackNum

                # caller che imposta il logger (inizio funzione)
                caller = inspect.stack()[2]
                dummy, programFile, lineNumber, funcName, lineCode, rest = caller
                modName = os.path.splitext(os.path.basename(programFile))[0]
                func = modName+'.'+funcName
                func = 'self.'+funcName
                data = TAB*' ' + '[called by: {FUNC}:{LINENO}]'.format(FUNC=func, LINENO=lineNumber)

                # caller che ha chiamato la funzione()
                caller = inspect.stack()[1]
                dummy, programFile, lineNumber, funcName, lineCode, rest = caller
                if funcName == '<module>': funcName = '__main__'
                str = "[{FUNC:<20}:{LINENO}] - {DATA}".format(FUNC=funcName, LINENO=lineNumber, DATA=data)
                print (str)
                '''
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



    isLoggerActive = False
    return nullLogger()


# ====================================================================================
# richiamando questa funzione posso dirottare l'out della log su CONSOLE previa
# impostazione del logger.ini con:
#
#        [logger_LnConsole]
#            handlers=consoleHandler
#            level=DEBUG
#            qualname=LnConsole
#            propagate=0
#
#  call: logger = gv.LN.consoleLOG(gv, __name__)
#  call: logger = gv.LN.consoleLOG(gv, __name__, funcName=sys._getframe().f_code.co_name)
#                   utile quando si hanno più funzioni all'interno dello stesso modulo
#
# ====================================================================================
# def SetLogger(gv, package, CONSOLE=None, stackNum=0):
def SetLogger(package, stackNum=0):
    # global isLoggerActive

    if _LOGGER:
        stackLevel = 1                          # stackLevel di base
        stackLevel += stackNum                  # aggiungiamo quello richiesto dal caller

        funcName    = sys._getframe(stackLevel).f_code.co_name
        funcLineNO  = sys._getframe(stackLevel).f_lineno
        if funcName == '<module>': funcName = '__main__'

        pkgName = package + '.' + funcName if funcName else package

        packageHier = pkgName.split('.')

        pkgName     = (packageHier[0] +'.'+packageHier[-1])  # se ho nomi servizi uguali in diversi moduli crea confusione
        pkgName     = ('.'.join(packageHier[-gPackageQualifiers:]))
        pkgName     = ('.'.join(packageHier[-2:])) # prende il modulo+Function

            # ------------------------------------------------
            # - del package prendiamo
            # - solo gli ultimi n.. gPackageQualifiers.
            # ------------------------------------------------
        if _logCONSOLE:
            pkgName = 'LnC.{0}'.format(package.split('.')[-1])


        # - tracciamo la singola funzione oppure modulo oppure libreria od altro
        LOG_LEVEL = None
        if _logMODULE:
            fullPkg = (package + funcName).lower()
            for stringa in _logMODULE:
                if stringa.lower() in fullPkg:
                    LOG_LEVEL = logging.DEBUG

        else:
            LOG_LEVEL = logging.DEBUG

    else:
        return SetNullLogger()


    logger = logging.getLogger(pkgName)

    # -----------------------------------------------------------------------------------------
    # - Per quanto riguarda il setLogger, devo intervenire sul numero di riga della funzione
    # - altrimenti scriverebbe quello della presente funzione.
    # - Per fare questo utilizzo l'aggiunta di un filtro passandogli il lineNO corretto
    # - per poi ripristinarlo al default
    # -----------------------------------------------------------------------------------------

    # print ('..........', LOG_LEVEL, pkgName)
    if not LOG_LEVEL:
        logger.disabled
        return logger

    logger.setLevel(LOG_LEVEL)
         # logger.setLevel(logging.NOTSET)  # oppure FATAL

        # - creiamo il contextFilter
    LnFilter    = ContextFilter()

        # - aggiungiamolo al logger attuale
    logger.addFilter(LnFilter)

        # - modifichiamo la riga della funzione chiamante
    LnFilter.setLineNO(funcLineNO)

        # ----------------------------------------------------------------------------------
        # - inseriamo la riga con riferimento al chiamante di questa fuznione
        # - nel "...called by" inseriamo il caller-1
        # ----------------------------------------------------------------------------------
    # logger.debug('')
    logger.debug('......called by:{CALLER}'.format(CALLER=_GetCaller(stackLevel+2)))

        # --------------------------------------------------------------------------
        # - azzeriamo il lineNO in modo che le prossime chiamate al logger, che
        # - non passano da questa funzione, prendano il lineNO corretto.
        # --------------------------------------------------------------------------
    LnFilter.setLineNO(None)
    LnFilter.setStack(5)            # ho verificato che con 5 sembra andare bene

    return logger




if __name__ == '__main__':
        # ---------------------------------------------------------
        # - SetUp del log
        # ---------------------------------------------------------
    userName=getpass.getuser()
    logFileName          = '/tmp/IFC_{USER}.log'.format(USER=userName)
    logConfigFileName   = os.path.join(os.path.dirname(__file__), 'LoggerConfig.ini')

    InitLogger(iniLogFile=logConfigFileName, logFileName=logFileName, package='IFC', packageQualifiers=2)
    logger = gv.Ln.setLogger(gv, package="Main")
