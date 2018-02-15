#!/usr/bin/python3.5
#
# updated by ...: Loreto Notarantonio
# Version ......: 15-02-2018 15.15.27
#
# -----------------------------------------------


from   Source.ParseInput.Main_ParseInput import ParseInput
from   Source.ParseInput.Main_ParseInput import EditPrjConfig

# from   Source.Main.CalculateRootDir import CalculateRootDir
from   Source.Main.CalculateRootDir import prepareEnv
from   Source.Main.Executor         import SetExecutor
from   Source.Main.TotalCommander   import SetTotalCommander

from   Source.Main.HostNames        import getHostName

from   Source.Main.WinScp           import SetWinSCP # bisogna ancora scrivere il file.ini
# from   Source.Main.WinScp           import SetWinSCP_rawsetting as SetWinSCP

from   . Setup import setProjectEnv   as SPE

