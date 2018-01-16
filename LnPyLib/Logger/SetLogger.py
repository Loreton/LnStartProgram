
import os
import inspect


class LnClass(): pass

from . LnLogger_Class import LnLogger


# ====================================================================================
# - dal package passato come parametro cerchiamo di individuare se la fuzione/modulo
# - è tra quelli da fare il log.
# - Il package mi server per verficare se devo loggare il modulo o meno
# ====================================================================================
def SetLogger(package, reset=False):

    pointers = LnLogger.static_getMainPointers()


    logger        = pointers.logger
    _LnFilter     = pointers.LnFilter
    _modulesToLog = pointers.modulesToLog
    _logLevel     = pointers.logLevel
    _nullLogger   = pointers.nullLogger

    fDEBUG = False



    ''' otteniamo i caller che ci servono '''
    CALLER = [1,2,3,4,5,6,7]
    CALLER[1] = GetCaller(1)
    # CALLER[2] = GetCaller(2)
    CALLER[3] = GetCaller(3)

        # ---------------------------------
        # - individuiamo se è un modulo
        # - da tracciare o meno
        # ---------------------------------
    fullPkg = (package + '.' + CALLER[1]._funcname)
    if '!ALL!' in _modulesToLog:
        LOG_LEVEL = _logLevel

    else:
        fullPkg_LOW = fullPkg.lower()
        LOG_LEVEL = None
        for moduleStr in _modulesToLog:
            if moduleStr.lower() in fullPkg_LOW:
                LOG_LEVEL = _logLevel


    if fDEBUG:
        print ('fullPkg   :', fullPkg )
        print ('LOG_LEVEL :', LOG_LEVEL )


    if not LOG_LEVEL:
        return _nullLogger

    logger.setLevel(LOG_LEVEL)

    _LnFilter.addStack(0)    # cambio lo stackNum

    if reset:
        logger.info('.... exiting\n')
    else:
        logger.info('.... entering called by: {CALLER}'.format(CALLER=CALLER[3]._fullcaller))

    # reset dello stackNum NON server se autoReset == True
    # _LnFilter.setStack(None)
    return logger



###############################################
#
###############################################
def GetCaller(stackLevel=0):
    retCaller = LnClass()
    retCaller._rcode  = 0

    try:
        dummy, programFile, lineNumber, funcName, lineCode, rest = inspect.stack()[stackLevel]

    except Exception as why:
        retCaller._fullcaller  = str(why)
        retCaller._rcode  = 1
        return retCaller   # potrebbe essere out of stack ma ritorniamo comunque la stringa


    if funcName == '<module>': funcName = '__main__'

    retCaller._funcname   = funcName
    retCaller._linecode   = lineCode
    retCaller._lineno     = lineNumber
    retCaller._fullfname  = programFile

    fname                   = os.path.basename(programFile).split('.')[0]
    retCaller._fname      = fname
    retCaller._fullcaller = "[{0}.{1}:{2}]".format(fname, funcName, lineNumber)

    return retCaller

