#!/usr/bin/env python3
# -*- coding: iso-8859-1 -*-

from  sys import version_info as sysVersion, path as sysPath, exit as sysExit
import platform
from pathlib import Path
'''
scriptMain  = Path(sys.argv[0]).resolve()
projectDir  = scriptMain.parent
currDir  = Path.cwd()
currDir  = Path('.').resolve()
print (scriptMain)
print (projectDir)
'''

# --------------------------------------------
# - inserire i path per fare l'import delle funzioni LnLib
# - ... sembra che non serva in quanto il path del progetto
# - ... è già inserito... comunque non si sa mai.
# --------------------------------------------
# LnLibDir    = Path(__file__).parent
# ProjectDir  = Path(LnLibDir).parent
# sysPath.insert(0, LnLibDir)
# sysPath.insert(0, ProjectDir)

if False:
    print ()
    # print (ProjectDir)
    # print (LnLibDir)
    # print (LnLibDir.joinpath('Common'))
    for path in sysPath: print (path)
    print ()
# sysExit()



# ############### OpSy type & version
# - sys.version_info(major=3, minor=3, micro=2, releaselevel='final', serial=0)
v = sysVersion
pyVer = '{0}{1}{2}'.format(v.major, v.minor, v.micro)
opSys = platform.system()
if opSys.lower() == 'windows':
    isWindows = True
else:
    isWindows = False
isUnix    = not isWindows
# ############### OpSy type & version

'''
from . LnCommon.LnLogger_New2                import SetLogger
from . LnCommon.LnLogger_New2                import InitLogger
# from . LnCommon.LnLogger                import SetNullLogger
from . LnCommon.LnColor                 import LnColor
from . LnCommon.Exit                    import Exit

from . System.GetKeyboardInput          import getKeyboardInput
from . System.ExecRcode                 import ExecRcode
from . LnMonkey import LnMonkeyFunctions
# from . LnMonkey import LnLoggerClass

from . LnDict.LnDict_DotMap             import DotMap  as LnDict

from . LnFile.ReadIniFile_Class         import ReadIniFile


# from . LnNet.InterfacesCl               import Interfaces
# from . LnNet.httpClient                 import httpGet


# from . LnFile.DirList                   import DirList
# from . LnFile.FileStatus                import FileModificationTime as Fmtime
# from . LnFile.ReadWriteTextFile         import readTextFile
# from . LnFile.ReadWriteTextFile         import writeTextFile


# from . SqLite.LnSqLite_Class                import LnSqLite


'''