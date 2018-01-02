#
# __author__  : 'Loreto Notarantonio'
# __version__ : '07-11-2017 14.10.09'
#


# migliore implementazione di pathlib.Path
#    https://pathpy.readthedocs.io/en/latest/
# from LnLib.File.LnPath import Path as Path
import sys, os
from pathlib import Path
'''
'''

#######################################################
# - facciamo l'import della LnLib
#######################################################
def setLnLibPath(libName, fDEBUG=False):

    zipFile       = '{}.zip'.format(libName)
    thisFile      = Path(sys.argv[0]).resolve()
    projectDir    = thisFile.parent
    extensionFile = thisFile.suffix.lower()
    myPath = []
    myPath.append(str(projectDir / 'bin' ))
    myPath.append(str(projectDir / 'lib' ))
    myPath.append(str(projectDir ))


    for path in myPath:
        zipFullName = Path(path) / zipFile
        if fDEBUG: print (zipFullName.exists(), zipFullName)
        if Path(zipFullName).exists():
            sys.path.append(str(zipFullName))  # deve essere una stringa e non WindowsPath
            break


    try:
        # import LnLib
        # oppure:
        import importlib # per importare un modulo come variabile
        Ln = importlib.import_module(libName)
    except ImportError as why:
        sys.stderr.write("\n")
        sys.stderr.write("      ERROR loading python module: " + libName + "\n")
        sys.stderr.write("      REASON: " + str(why) + "\n")
        sys.stderr.write("\n\n      LIBNAME {}.zip not FOUND in the following paths\n".format(libName))

        print()
        for path in myPath: print ('  ', path)
        print()
        for path in sys.path: print ('  ', path)
        print()
        sys.exit()


# setLnLibPath('LnLib')

LnLibPath = Path(sys.argv[0]).resolve().parent / 'bin/LnLib.zip'
sys.path.append(str(LnLibPath))  # deve essere una stringa e non WindowsPath

# import LnLib
# import LnLib.System.SetOsEnv      as  SetEnv
from  LnLib.System import SetOsEnv      as  OsEnv

from LnLib.Common.LnLogger import init as initLogger

# from LnLib.Common.LnLogger        import InitLogger

from LnLib.Common.Exit            import Exit        as LnExit
from LnLib.Dict.LnDict_DotMap     import DotMap      as LnDict
from LnLib.File.ReadIniFile_Class import ReadIniFile as LnReadIniFile

from LnLib.System.RunProgram      import RunProgram  as runProgram







