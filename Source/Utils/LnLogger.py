#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

# updated by ...: Loreto Notarantonio
# Version ......: 19-06-2019 18.20.43
#
# 05-11-2018: creato _printLog unico sia per console che per log
#
import sys, os, time
import json, yaml
if sys.version_info >= (3,0):
    unicode = str

###########################################
# - converte LnClass o LnDict in dict
###########################################
def toDict(data):
    # print (type(data))
    _myDict = {}
    dataType = str(type(data)).lower()

    if 'dotmap' in dataType:
        print ('dotamp')
        _myDict = data.toDict()


    elif 'lnclass' in dataType:
        print ('lnclass')
        for item in vars(data):
            _myDict[item] = getattr(data, item)

    else:
        _myDict = data

    return _myDict



##############################################################################
# - classe che mi permette di lavorare nel caso il logger non sia richiesto
##############################################################################
class nullLogger():
    def __init__(self, log_modules=[]):
        self._log_modules = log_modules
        pass

    def dummy(self,  title, extra_data=''): pass
    info    = dummy
    debug   = dummy
    debug1  = dummy
    debug2  = dummy
    debug3  = dummy
    error   = dummy

    def console(self,  title, extra_data=''):
        caller = _getCaller(stackNum=2, modules=self._log_modules)
        if not caller:
            return

        console_prefix = "{} -> ".format(caller)

        data = prepareData(title, extra_data)
        for line in data:
            print(console_prefix + line)


class myLogger():
    def __init__(self, filename, debug_level=-1, dry_run=False, log_modules=[], color=None):
        global C
        self._debugLevel        = debug_level
        self._date_time_format  = '%m-%d %H:%M:%S'
        self._dry_run = dry_run
        self._log_modules = log_modules
        C = color

        # if filename:
        self.logger = open(filename,'w', encoding='utf-8')
            # Messaggio iniziale nel LOG
        self._printLog('INFO', '\n'*5,
                [
                    '-'*50,
                    '- starting: ' + time.strftime("%Y/%m/%d %H:%M:%S"),
                    '- dry-run:     ' + str(dry_run),
                    '- debug level: ' + str(debug_level),
                    '-'*50,
                    ''
                ])


    def _printLog(self, level=None, title=None, extra_data=''):
        caller = _getCaller(stackNum=3, modules=self._log_modules)
        if not caller:
            return

        now = time.strftime("%Y/%m/%d %H:%M:%S")
        disp_level = level[:4]
        if self._dry_run:
            disp_level = disp_level + '-DR'

        log_prefix = "{} - {} {} -> ".format(now, caller, disp_level)
        console_prefix = "{} -> ".format(caller)
        data = prepareData(title, extra_data)
        for line in data:
            if level in ['CONSOLE']:
                if C:
                    C.printColored(C.yellow, text=console_prefix, end='')
                    C.printColored(C.yellowH, text=line)
                else:
                    print(console_prefix + line)
                self.logger.write(log_prefix + line + '\n')
            else:
                self.logger.write(log_prefix + line + '\n')

        self.logger.flush()  #  by Loreto:  01-11-2018 18.55.13



        # extra_data può essere tuple, list, str o altro da verificare
    def info(self,  title, extra_data=''):
        assert isinstance(title, (str, unicode))
        self._printLog('INFO', title, extra_data=extra_data)


    def debug(self,  title, extra_data=''):
        assert isinstance(title, (str, unicode))
        if self._debugLevel >= 0:
            self._printLog('DBG', title, extra_data=extra_data)

    def debug1(self,  title, extra_data=''):
        assert isinstance(title, (str, unicode))
        if self._debugLevel >= 1:
            self._printLog('DBG1', title, extra_data=extra_data)

    def debug2(self,  title, extra_data=''):
        assert isinstance(title, (str, unicode))
        if self._debugLevel >= 2:
            self._printLog('DBG2', title, extra_data=extra_data)

    def debug3(self,  title, extra_data=''):
        assert isinstance(title, (str, unicode))
        if self._debugLevel >= 3:
            self._printLog('DBG3', title, extra_data=extra_data)

    def error(self,  title, extra_data=''):
        self._printLog('ERROR', title, extra_data=extra_data)

    def console(self, title, extra_data=''):
        self._printLog('CONSOLE', title, extra_data=extra_data)

    def _dummy(self, level=None, title=None, extra_data=''):
        pass



def _getCaller(stackNum=3, modules=[]):
    caller = sys._getframe(stackNum)
    programFile = caller.f_code.co_filename
    lineNumber  = caller.f_lineno
    funcName    = caller.f_code.co_name

    if funcName == '<module>': funcName = '__main__'
    fname = os.path.basename(programFile).split('.')[0]
    pkg = funcName
    pkg = fname + '.' + funcName
    pkg = pkg.replace('ansible_module_', '')

    FOUND = False
    if modules in ([], ['*'], ['all']):
        FOUND = True
    else:
        for module in modules:
            if module in pkg:
                FOUND = True

    if FOUND:
        _caller = "[{FUNC:<15}:{LINENO:4}]".format(FUNC=pkg, LINENO=lineNumber)
    else:
        _caller = None

    return _caller


def prepareData(title, extra_data):
    data_list = []
    TAB=4*' '
    '''
    if extra_data in ['xxx', 'xxx']:  # devo evitare  None e False
        data_list.append(title)
        data_list.append(str(extra_data))

    else:
    '''
    if isinstance(extra_data, list) or isinstance(extra_data, tuple):
        data_list.append(title + ' [list={}]:'.format(len(extra_data)))
        if len(extra_data):
            for index, item in enumerate(extra_data):
                data = '{}[{:04}] - {}'.format(TAB, index, item)
                data_list.append(data)
        else:
            data = '{}- []'.format(TAB)
            data_list.append(data)

    elif isinstance(extra_data, dict): # ance DotMap?
        data_list.append(title + '[dict]:')
        my_json = json.dumps(extra_data, indent=4, sort_keys=True)
        my_yaml = yaml.dump(yaml.load(my_json), default_flow_style=False)
        for line in my_json.split('\n'):
            data_list.append(line)

    elif isinstance(extra_data, bool):
        data = '{}: {}'.format( title, str(extra_data))
        data_list.append(data)

    elif extra_data in ['']:
        data_list.append(title)

    else:
        data = '{}: {}'.format(title, extra_data)
        data_list.append(data)

    return data_list



def setLogger(filename=None, debug_level=0, dry_run=False, log_modules=[], color=None):
    if filename:
        return myLogger(filename, debug_level, dry_run, log_modules, color)
    else:
        return nullLogger(log_modules)

