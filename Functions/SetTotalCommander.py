#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
# updated by Loreto: 17-10-2017 08.34.07
# -----------------------------------------------
import sys, os

logger = None


# =============================================
# = Parsing
# =============================================
def SetTotalCommander(gv):
    global logger
    logger = gv.logger
    CMDList = []
    TCDir  = '{}\Files\Manager\WinCmd-LN'.format(gv.Ln.FreeDir)
    TCexe  = '{}\realApp\WinCmd\TOTALCMD.EXE'.format(TCDir)

    dataDir      = setVerifyPath('{}\LnData'.format(TCDir))
    TCIconsDir   = setVerifyPath('{}\Icons'.format(dataDir))
    TCIConfigDir = setVerifyPath('{}\Config'.format(dataDir))

    tcIniFile    = setVerifyPath('{}\Wincmd.ini'.format(TCIConfigDir))
    ftpIniFile   = setVerifyPath('{}\Wcx_Ftp.ini'.format(TCIConfigDir))
    logDir       = setVerifyPath('{}\log'.format(dataDir))

    # if  not os.path.isfile(tcIniFile) \
    #     or not os.path.isfile(ftpIniFile) \
    #     or not os.path.isfile(TCexe) \
    #     or not os.path.isdir(logDir):
    #     print('ERRORE....')
    #     sys.exit()


    CMDList.append(TCexe)
    CMDList.append('/I={}'.format(tcIniFile))
    CMDList.append('/F={}'.format(ftpIniFile))
    return CMDList



'''
e:\LnED\Lacie232\Filu\LnDisk\LnFree\Files\Manager\WinCmd-LN\realApp\WinCmd\TOTALCMD.EXE
e:\LnED\Lacie232\Filu\LnDisk\LnFree\Files\Manager\WinCmd-LN\Files\Manager\WinCmd-LN\LnData\Config\Wincmd.ini
rem ####################################################
rem # :Process
rem ####################################################
:Process
    echo "TotalCommander: Ln.FreeDir = %Ln.FreeDir%"

    set "TCPATH=%~dp0"
    set "Ln.TC_PATH=%TCPATH:~0,-1%"             &:: --- togli ultimo char '\'
    cd /D "%Ln.TC_PATH%"
    echo "Current directory:   %CD%"

    set "Ln.TC_IconsDIR=%Ln.TC_PATH%\LnData\Icons"
    set "Ln.TC_ConfigDIR=%Ln.TC_PATH%\LnData\Config"
    set "PrgDir=%Ln.TC_PATH%\realApp\Wincmd"
    set "TC_iniFile=%Ln.TC_PATH%\LnData\Config\Wincmd.ini"
    set "TC_Ftp_iniFile=%Ln.TC_PATH%\LnData\Config\Wcx_Ftp.ini"
    set "TC_LogDir=%Ln.TC_PATH%\LnData\log"
    set "sr=python %Ln.GitRepodir%\Python3\LnPythonLib\LnTools\ReplaceTextInFiles.py"

    set "TC_Program==%PrgDir%\TOTALCMD.exe" && set "MSG=Stiamo lavorando con TotalCommander 32 Bits"
    if /I "%OS%"       == "64BIT"  set "TC_Program==%PrgDir%\TOTALCMD64.exe" && set "MSG=Stiamo lavorando con TotalCommander 64 Bits"
    if /I "%OS%"       == "64Bits" set "TC_Program==%PrgDir%\TOTALCMD64.exe" && set "MSG=Stiamo lavorando con TotalCommander 64 Bits"
    if    "%OSBits%"   == "64"     set "TC_Program==%PrgDir%\TOTALCMD64.exe" && set "MSG=Stiamo lavorando con TotalCommander 64 Bits"

    echo "%MSG%"
    echo.
    echo.
    set "CMD=%TC_Program% /I=%TC_iniFile% /F=%TC_Ftp_iniFile%"
    echo %CMD%
    echo.
    start %CMD%
    :: start %TC_Program% /I=%TC_iniFile% /F=%TC_Ftp_iniFile%

    REM start %PrgDir%\TOTALCMD.exe /I=%TC_iniFile% /F=%TC_Ftp_iniFile%
    REM start %PrgDir%\TOTALCMD64.exe /I=%TC_iniFile% /F=%TC_Ftp_iniFile%

    :: pause
    echo "sleeping for 5 sec..." && sleep 5


'''

