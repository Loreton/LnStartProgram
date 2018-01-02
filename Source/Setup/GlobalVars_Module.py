#!/usr/bin/python3.5
#
# updated by ...: Loreto Notarantonio
# Version ......: 02-01-2018 09.22.07
#

# -----------------------------------------------
'''
    1. Provvede a caricare la LnLib
    2. ospiterà tutte le variabili globali per il progetto
'''

import sys
from pathlib import Path

######### SET LIB PATH per la libreria LnLib #######################
######### SET LIB PATH per la libreria LnLib #######################
######### SET LIB PATH per la libreria LnLib #######################
def LibPath(libName, fDEBUG=True):
    thisFile      = Path(sys.argv[0]).resolve()
    # projectDir    = thisFile.parent
    extensionFile = thisFile.suffix.lower()

    if extensionFile.lower() == '.zip':
        print ('libName:', libName)
        LnLibPath = Path(sys.argv[0]).resolve().parent / 'bin' / libName
    else:
        LnLibPath = Path(sys.argv[0]).resolve().parent
        # LnLibPath = Path('y:\GIT-REPO\Python3\LnPythonLib\@LNLIB_BASE')
        print(' loading LnLibrary from Source directory.....')

    sys.path.insert(0, str(LnLibPath))  # deve essere una stringa e non WindowsPath
    import LnLib

    return LnLib
######### SET LIB PATH per la libreria LnLib #######################
######### SET LIB PATH per la libreria LnLib #######################
######### SET LIB PATH per la libreria LnLib #######################



def LnClass():
    pass
    def __str__(self):
        _str_ = []
        for key,val in self.__dict__.items():
            _str_.append('{:<15}: {}'.format(key, val))

        return '\n'.join(_str_)
