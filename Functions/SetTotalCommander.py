#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
# updated by Loreto: 19-10-2017 15.59.48
# -----------------------------------------------
from    sys import exit as sysExit
import os
import winreg

# =============================================
# = Parsing
# =============================================
def SetTotalCommander(gv):
    logger = gv.Ln.SetLogger(__package__)
    CMDList = []
    TCDir     = gv.Ln.VerifyPath(gv, gv.env.FreeDir.joinpath('Files/Manager/WinCmd-LN'))
    dataDir   = gv.Ln.VerifyPath(gv, TCDir.joinpath('LnData'))
    iconsDir  = gv.Ln.VerifyPath(gv, TCDir.joinpath('LnData/Icons'))
    configDir = gv.Ln.VerifyPath(gv, TCDir.joinpath('LnData/Config'))
    logDir    = gv.Ln.VerifyPath(gv, TCDir.joinpath('log'))

    tcIniFile  = gv.Ln.VerifyPath(gv, configDir.joinpath('WinCmd.ini'))
    ftpIniFile = gv.Ln.VerifyPath(gv, configDir.joinpath('Wcx_Ftp.ini'))




    # =====================================================================
    # * Verifichiamo la versione del sistema operativo
    # * Set "RegQry=HKLM\Hardware\Description\System\CentralProcessor\0"
    # * "%SystemRoot%\system32\REG.exe"  Query %RegQry%
    # =====================================================================
    reg_obj = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'Hardware\Description\System\CentralProcessor\0',0, (winreg.KEY_WOW64_64KEY+ winreg.KEY_READ))
    OSbits = winreg.EnumValue(reg_obj, 1)[1].split()[0]   # ('Identifier', 'Intel64 Family 6 Model 69 Stepping 1', 1)
    winreg.CloseKey(reg_obj)
    logger.info("Windows OS bits: {}".format(OSbits))

    if OSbits.lower() == "intel64":
        TCexe = gv.Ln.VerifyPath(gv, TCDir.joinpath('realApp/WinCmd/TOTALCMD64.exe'))
        if gv.fDEBUG: print ("Stiamo lavorando con TotalCommander 64 Bits")
    else:
        TCexe = gv.Ln.VerifyPath(gv, TCDir.joinpath('realApp/WinCmd/TOTALCMD.exe'))
        if gv.fDEBUG: print ("Stiamo lavorando con TotalCommander 32 Bits")


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

