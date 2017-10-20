#!/usr/bin/env python3
# -*- coding: iso-8859-1 -*-

import sys, os
import platform



# ############### OpSy type & version
# - sys.version_info(major=3, minor=3, micro=2, releaselevel='final', serial=0)
v = sys.version_info
pyVer = '{0}{1}{2}'.format(v.major, v.minor, v.micro)
opSys = platform.system()
if opSys.lower() == 'windows':
    isWindows = True
else:
    isWindows = False

isUnix    = not isWindows
# ############### OpSy type & version


from . LnCommon.LnLogger                import SetLogger
from . LnCommon.LnLogger                import InitLogger
from . LnCommon.LnLogger                import SetNullLogger
from . LnCommon.LnColor                 import LnColor
from . LnCommon.Exit                    import Exit

from . System.GetKeyboardInput          import getKeyboardInput
from . System.ExecRcode                 import ExecRcode

from . LnDict.LnDict_DotMap             import DotMap  as LnDict

from . LnFile.ReadIniFile_Class         import ReadIniFile


# from . LnNet.InterfacesCl               import Interfaces
# from . LnNet.httpClient                 import httpGet


# from . LnFile.DirList                   import DirList
# from . LnFile.FileStatus                import FileModificationTime as Fmtime
# from . LnFile.ReadWriteTextFile         import readTextFile
# from . LnFile.ReadWriteTextFile         import writeTextFile


# from . SqLite.LnSqLite_Class                import LnSqLite


