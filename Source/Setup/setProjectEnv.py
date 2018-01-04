#!/usr/bin/python3.5
#
# updated by ...: Loreto Notarantonio
# Version ......: 04-01-2018 15.58.19
#

# -----------------------------------------------
'''
    1. Provvede a caricare la LnLib
    2. ospiterà tutte le variabili globali per il progetto
'''

import  sys
from    pathlib import Path
import  importlib

####################################################################
# SET LIB PATH per la libreria LnLib
####################################################################
def LibPath(myLibName, fDEBUG=True):
    assert type(myLibName) == list
    '''
        insert the correct path to allow import of the libraryName passed.
        it works with myLib as directory or myLib.zip

        myLibName[0]  = name to be imported
        myLibName[1]  = may be zip version of libraries
        myLibName[..] = may be zip version of libraries
    '''
    thisfile = Path(sys.argv[0]).resolve()

    thisDir  = thisfile.parent
    thisExt  = thisfile.suffix.lower()
    if fDEBUG:
        print ('thisDir:', thisDir)
        print ('thisExt:', thisExt)

    myPaths = []
    for lib in myLibName:
        libName = Path(lib)
        libExt  = libName.suffix.lower()

        if fDEBUG:
            print ('libName:', libName)
            print ('libExt:', libExt)

        if thisExt == '.zip':
            myPaths.append(Path(thisDir) / libName)

        elif libExt == '.zip':
            myPaths.append(Path(thisDir) / 'bin' / libName)

        else:
            myPaths.append(thisDir)

    for path in myPaths:
        if fDEBUG: print ('path:', path)
        sys.path.insert(0, str(path))  # deve essere una stringa e non WindowsPath

    # load library with name in variable string
    myLib = importlib.import_module(myLibName[0])
    # import LnLib

    return myLib







def LnClass():
    pass
    def __str__(self):
        _str_ = []
        for key,val in self.__dict__.items():
            _str_.append('{:<15}: {}'.format(key, val))

        return '\n'.join(_str_)
