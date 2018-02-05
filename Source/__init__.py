#!/usr/bin/python3.5
#
# updated by ...: Loreto Notarantonio
# Version ......: 02-02-2018 10.26.21
#
# -----------------------------------------------


from   Source.ParseInput.Main_ParseInput import ParseInput

# from   Source.Main.CalculateRootDir import CalculateRootDir
from   Source.Main.CalculateRootDir import prepareEnv
from   Source.Main.Executor         import SetExecutor
from   Source.Main.TotalCommander   import SetTotalCommander

from   Source.Main.HostNames        import getHostName

from   Source.Main.WinScp           import SetWinSCP # bisogna ancora scrivere il file.ini
# from   Source.Main.WinScp           import SetWinSCP_rawsetting as SetWinSCP

from   . Setup import setProjectEnv   as SPE

