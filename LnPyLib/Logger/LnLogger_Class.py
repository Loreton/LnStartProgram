import sys
# from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
import logging
from logging import handlers  # se non lo inserisco da errore sull'handlers
from pathlib import Path
import inspect


class LnClass(): pass

'''
# https://stackoverflow.com/questions/20372669/python-use-the-same-class-instance-in-multiple-modules
def singleton_with_args(*args, **kwargs):
    def wrapper(cls):
        return cls(*args, **kwargs)
    return wrapper


# https://stackoverflow.com/questions/39492471/how-to-extend-the-logger-logging-class
# https://stackoverflow.com/questions/19615876/showing-the-right-funcname-when-wrapping-logger-functionality-in-a-custom-class
@singleton_with_args(0)
'''
class LnLogger(logging.getLoggerClass()):
    ''' LnLogger class '''

        # ----------------------------------------------------------------------------
        # - variabili che saranno condivise da tutti i chiamanti.
        # - inserisco i pointer ed i valori basilari per condividere la classe
        # ----------------------------------------------------------------------------
    loggers    = set() # univoco MA... non mantiene l'ordine di iserimento
    Pointers   = LnClass()

    def __init__(   self,
                    name='LnLoggerClass',
                    toFILE=False,
                    toCONSOLE=False,
                    logfilename=None,
                    defaultLogLevel='info',
                    ARGS=None,
                    rotationType='time',
                    backupCount=5,
                    maxBytes=20000,
                    when="m",
                    interval=60,
                    ):


        ''' internal variables '''
        self._logEnabled        = False
        self._level             = logging.INFO

        self._name              = name
        self._to_file           = False
        self._to_console        = False
        self._filename          = None
        self._modulesToLog      = []

        self._rotation_type     = rotationType
        self._backup_count      = backupCount
        self._max_bytes         = maxBytes
        self._when_rotate       = when
        self._rotation_interval = interval

        self._file_format       = '[%(asctime)s] [%(LnFuncName)-20s:%(lineno)4d] %(levelname)-5.5s - %(message)s'
        self._console_format    = '[%(LnFuncName)-20s:%(lineno)4d] %(levelname)-5.5s - %(message)s'
        # self._file_format       = '[%(asctime)s] [%(module)-20s:%(lineno)4d] %(levelname)-5.5s - %(message)s'
        # self._console_format    = '[%(module)-20s:%(lineno)4d] %(levelname)-5.5s - %(message)s'
        self._date_time_format  = '%m-%d %H:%M:%S'

        self._myLogger          = logging.getLogger(self._name)
        self._nullLogger        = nullLogger()
        self._LnFilter          = ContextFilter(defaultStack=6, autoReset=True)

        if name not in self.loggers:
            self.loggers.add(name)
            self._myLogger.setLevel(self._level)
            self._myLogger.addFilter(self._LnFilter)

        self._LnFilter.setFuncName('initializing')

        ''' setting LogLevel '''
        assert type(defaultLogLevel) == str
        if   defaultLogLevel.lower() == 'debug':    self._level = logging.DEBUG
        elif defaultLogLevel.lower() == 'warning':  self._level = logging.WARNING



        ''' setting file/console/logEnable/modulesToLog '''
        self._prepareFileLog(toFILE, logfilename)

        ''' put Console to override file settings '''
        self._prepareConsoleLog(toCONSOLE)

        ''' prepare logfile if required '''
        if self._to_file or self._to_console:
            self._logEnabled = True
            self.logger = self._myLogger
        else:
            self.logger = self._nullLogger


            # ---------------------------------------------
            # - inseriamo alcuni puntatori per permettere
            # - agli altri di accedere alla stessa istanza
            # - di logger
            # ---------------------------------------------
        self.Pointers.rootName     = self._name
        self.Pointers.logger       = self.logger
        self.Pointers.LnFilter     = self._LnFilter
        self.Pointers.modulesToLog = self._modulesToLog
        self.Pointers.logLevel     = self._level
        self.Pointers.nullLogger   = self._nullLogger



        self._myLogger.setLevel(self._level)
        self.info('initialised.....')
        # self._LnFilter.setFuncName(None) # reset al nome del modulo chiamante




    ##############################################################
    #
    ##############################################################
    def _prepareConsoleLog(self, toCONSOLE):
        ''' provides:
                create consoleHandler
                add consoleHandler to logger
        '''

        if toCONSOLE==False:
            self._to_console = False
            return

        elif toCONSOLE==[]:
            self._to_console = True
            self._modulesToLog = ['!ALL!']

        elif toCONSOLE:
            self._to_console = True
            self._modulesToLog = toCONSOLE


            ''' prepare log to console if required '''
        _consoleFormatter = logging.Formatter(fmt=self._console_format, datefmt=self._date_time_format)
        _consoleHandler   = logging.StreamHandler(stream=sys.stdout)
        _consoleHandler.setFormatter(_consoleFormatter)
        self._myLogger.addHandler(_consoleHandler)





    ##############################################################
    #
    ##############################################################
    def _prepareFileLog(self, toFILE, logfilename):
        ''' provides:
                open file
                set rotation policy
                create fileHandler
                add fileHandlet to logger
        '''

        if toFILE==False:
            self._to_file = False
            return


        if toFILE==[]:
            self._to_file = True
            self._modulesToLog = ['!ALL!']

        elif toFILE:
            self._to_file = True
            self._modulesToLog = toFILE



        _LOG_DIR = Path(logfilename).parent
        self._filename = logfilename

        try:
            _LOG_DIR.mkdir(parents=True)
        except (FileExistsError):           # skip error if exists
            pass

        print ('logFile:', str(self._filename))

        if self._rotation_type == 'time':
            fileHandler = handlers.TimedRotatingFileHandler(
                            str(self._filename),
                            when=self._when_rotate,
                            interval=self._rotation_interval,
                            backupCount=self._backup_count
                        )

        elif self._rotation_type == 'size':
            fileHandler = handlers.RotatingFileHandler(
                            str(self._filename),
                            maxBytes=self._max_bytes,
                            backupCount=self._backup_count
                        )

        else:
            fileHandler = logging.FileHandler(self._filename)

        fileFormatter = logging.Formatter(fmt=self._file_format, datefmt=self._date_time_format)
        fileHandler.setFormatter(fileFormatter)
        self._myLogger.addHandler(fileHandler)




    ##############################################################
    #
    ##############################################################
    @staticmethod
    def static_getMainPointers():
        return LnLogger.Pointers




    ##############################################################
    #
    ##############################################################
    def info(self, msg, extra=None):
        self.logger.info(msg)
        # self.logger.info(msg, extra=extra)

    def error(self, msg, extra=None):
        self.logger.error(msg)
        # self.logger.error(msg, extra=extra)

    def debug(self, msg, extra=None):
        self.logger.debug(msg)
        # self.logger.debug(msg, extra=extra)

    def warn(self, msg, extra=None):
        self.logger.warn(msg)
        # self.logger.warn(msg, extra=extra)


    # ====================================================================================
    # - dal package passato come parametro cerchiamo di individuare se la fuzione/modulo
    # - è tra quelli da fare il log.
    # - Il package mi server per verficare se devo loggare il modulo o meno
    # ====================================================================================
    @classmethod   # permette il richiamo senza dover inizializzare la classe
    def SetLoggerCM(cls, package, stackNum=0, reset=False):
        # xx = LnLogger()
        # myLogger = xx.logger
        # print (cls._name)
        # print (cls.loggers)
        # print (cls._to_console)
        myLogger = cls.class_getlogger()
        return myLogger




##############################################################################
# - classe che mi permette di lavorare nel caso il logger non sia richiesto
##############################################################################
class nullLogger():
    def __init__(self, package=None, stackNum=1, extra=None): pass
    def info(self, data):       self._dummy(data)
    def debug(self, data):      self._dummy(data)
    def error(self, data):      self._dummy(data)
    def warning(self, data):    self._dummy(data)
    def _dummy(self, data): pass

    '''
    def _print(self, data, stackNum=2):
        TAB = 4
        data = '{0}{1}'.format(TAB*' ',data)
        caller = inspect.stack()[stackNum]
        dummy, programFile, lineNumber, funcName, lineCode, rest = caller
        if funcName == '<module>': funcName = '__main__'
        pkg = package.split('.', 1)[1] + '.' +funcName
        str = "[{FUNC:<20}:{LINENO}] - {DATA}".format(FUNC=pkg, LINENO=lineNumber, DATA=data)
        print (str)
    '''



##############################################################
# http://stackoverflow.com/questions/16203908/how-to-input-variables-in-logger-formatter
##############################################################
class ContextFilter(logging.Filter):
    """
    This is a filter which injects contextual information into the log.

    Rather than use actual contextual information, we just use random
    data in this demo.
    """
    def __init__(self, defaultStack=5, autoReset=False):
        '''
        defaultStack=5 sembra OK
        '''
        self._defaultStack  = defaultStack
        self._line          = None
        self._name          = None
        self._LnFuncName    = None      # creata da me
        self._stack         = defaultStack
        self._fDEBUG        = False
        self._autoReset     = autoReset
        '''
        ho verificato che con 5 sembra andare bene
        usato quando chiamato direttamete dal logger
        quando lo chiamo dal SetLogger devo impostaro a 6
        '''


    def setAutoReset(self, flag):
        self._autoReset = flag

    def setLineNO(self, number):
        self._line = number

    def setFuncName(self, myname):
        self._LnFuncName = myname

    def setStack(self, number):
        self._stack = number if number else self._defaultStack

    def addStack(self, number):
        self._stack = (self._defaultStack + number) if number else self._defaultStack
        # print ('self._stack changed to:', self._stack)

    def filter(self, record):
        dummy, programFile, lineNO, funcName, lineCode, rest = inspect.stack()[self._stack]
        if self._autoReset: self._stack = self._defaultStack

        if funcName == '<module>': funcName = '__main__'

            # - modifica della riga
        if self._line:
            record.lineno = self._line
            if self._autoReset: self._line = None
        else:
            record.lineno = lineNO

            # - modifica della LnFuncName
        if self._LnFuncName:
            record.LnFuncName = self._LnFuncName
            if self._autoReset: self._LnFuncName = None
        else:
            record.LnFuncName = funcName


            # - modifica del name
        if self._name:
            record.name = self._name
            if self._autoReset: self._name = None
        else:
            record.name = funcName


        return True


