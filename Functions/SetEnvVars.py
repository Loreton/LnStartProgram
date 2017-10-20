#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
# updated by Loreto: 20-10-2017 15.25.31
#  https://docs.python.org/3/library/pathlib.html
# -----------------------------------------------
from    os     import environ, getenv
from    sys     import exit as sysExit
from    pathlib import Path, PurePath

logger = None
#########################################################################
#
#########################################################################
def setOsEnv(varName, varValue):
    msg = '{0:<20} : {1}'.format(varName, varValue)
    logger.info(msg)
    if gv.fDEBUG: print (msg)
    environ[varName] = str(varValue)

#########################################################################
#
#########################################################################
def setPath(pathName):
    logger.info('{0:<20} : {1}'.format(pathName))


#########################################################################
#
#########################################################################
def SetEnvVars(gVars):
    global gv, logger
    gv = gVars
    logger = gv.prj.SetLogger(__name__)


    iniFile = gv.Ln.ReadIniFile(gv.args.config_file, strict=True)
    iniFile.setDebug(False)
    iniFile.read(resolveEnvVars=True)
    gv.cfgFile = gv.Ln.LnDict(iniFile.dict)
    # gv.cfgFile.printTree(fPAUSE=True)




    sysExit()

#########################################################################
#
#########################################################################
def SetEnvVars_OK(gVars):
    global gv, logger
    gv = gVars
    logger = gv.prj.SetLogger(__name__)


    freeDir     = gv.env.FreeDir
    rootDir     = gv.env.RootDir
    gitRepoDir  = gv.env.GitRepoDir
    pythonDir   = gv.prj.VerifyPath(gv, freeDir.joinpath('Pgm/WinPython-64bit-3.5.3.1Qt5/python-3.5.3.amd64'))
    JAVA_HOME   = gv.prj.VerifyPath(gv, freeDir.joinpath('Pgm/Java/jdk1.8.0_66'))


    myVars = {
        'Ln.BdiDir'             : PurePath('d:/Dati/Profili/f602250/Documents'),
        'Ln.PortableAppsDir'    : rootDir.joinpath('PortableApps\PortableApps'),
        'Ln.PythonDir'          : pythonDir,
        'JAVA_HOME'             : JAVA_HOME,

              # *****************************************
              # -      Programmi specifici
              # *****************************************
        'Ln.NOTEPAD++'          : freeDir.joinpath('Editors/NotePad++/notepad++.exe'),
        'Ln.SublimeEditor'      : freeDir.joinpath('Editors/SublimeText_3/sublime_text.exe'),
        'Ln.myEditor'           : freeDir.joinpath('Editors/SublimeText_3/sublime_text.exe'),
        'Ln.KittyEXE'           : freeDir.joinpath('Network/Telnet/Kitty/Kitty.exe'),
        'Ln.WinScpEXE'          : freeDir.joinpath('Network\FTPc\WinSCP\winscp.exe'),
        'Ln.PythonExe'          : pythonDir.joinpath('python.exe'),

        "Ln.WinScpKittyCmd"     : gitRepoDir.joinpath("Scripts/python/Sources/KittyFromWinScp/bin/kitty-from-WinScp.cmd"),
        "Ln.WinScpKittyPy"      : gitRepoDir.joinpath("Scripts/python/Sources/KittyFromWinScp/__main__.py"),
    }

    for varName, varValue in myVars.items():
        setOsEnv(varName, gv.prj.VerifyPath(gv, varValue))


    myPATH = []
    myPATH.append(pythonDir)
    myPATH.append(pythonDir.joinpath("DLLs"))
    myPATH.append(pythonDir.joinpath("Lib"))
    myPATH.append(pythonDir.joinpath("Scripts"))
    myPATH.append(pythonDir.joinpath("Lib/site-packages"))
    myPATH.append(pythonDir.joinpath("Lib/site-packages/win32com"))

    myPATH.append(JAVA_HOME.joinpath("bin"))

    myPATH.append(gitRepoDir.joinpath("GIT-PRG/PortableGit-2.11.0/bin"))
    myPATH.append(freeDir.joinpath("SynchBackup/cwRsync/bin"))
    myPATH.append(freeDir.joinpath("Network/OpenSSH_60/bin"))
    myPATH.append(freeDir.joinpath("Network/Telnet/Putty"))
    myPATH.append(freeDir.joinpath("cygwin64/bin"))
    myPATH.append(freeDir.joinpath("Network/openSSL"))


    newPATH = getenv('PATH')
    if gv.fDEBUG:
        print ()
        print (newPATH)

    for path in reversed(myPATH):
        path = '{0};'.format(path)
        newPATH = newPATH.replace(path, '')
        newPATH = path + newPATH

    if gv.fDEBUG:
        print ()
        print (newPATH)

    environ['PATH'] = newPATH



    '''
    setOsEnv('',  gv.Ln.VerifyPath(gv, rootDir.joinpath('')))
    setOsEnv('',  gv.Ln.VerifyPath(gv, rootDir.joinpath('')))
    setOsEnv('',  gv.Ln.VerifyPath(gv, rootDir.joinpath('')))
    setOsEnv('',  gv.Ln.VerifyPath(gv, rootDir.joinpath('')))
    '''

    # sysExit()




    '''
    myVars = {
        'Ln.BdiDir'             : gv.Ln.VerifyPath(gv, PurePath('d:/Dati/Profili/f602250/Documents2'), exitOnError=False),
        'Ln.PortableAppsDir'    : gv.Ln.VerifyPath(gv, rootDir.joinpath('PortableApps\PortableApps')),
        'Ln.PythonDir'          : pythonDir,


        'JAVA_HOME'             : JAVA_HOME,

              # *****************************************
              # -      Programmi specifici
              # *****************************************
        'Ln.NOTEPAD++'          : gv.Ln.VerifyPath(gv, freeDir.joinpath('Editors/NotePad++/notepad++.exe')),
        'Ln.SublimeEditor'      : gv.Ln.VerifyPath(gv, freeDir.joinpath('Editors/SublimeText_3/sublime_text.exe')),
        'Ln.myEditor'           : gv.Ln.VerifyPath(gv, freeDir.joinpath('Editors/SublimeText_3/sublime_text.exe')),

        'Ln.KittyEXE'           : gv.Ln.VerifyPath(gv, freeDir.joinpath('Network/Telnet/Kitty/Kitty.exe')),
        'Ln.WinScpEXE'           : gv.Ln.VerifyPath(gv, freeDir.joinpath('Network\FTPc\WinSCP\winscp.exe')),
        'Ln.PythonExe'           : gv.Ln.VerifyPath(gv, pythonDir.joinpath('python.exe')),

        'Ln.BdiDir'             : gv.Ln.VerifyPath(gv, PurePath('d:/Dati/Profili/f602250/Documents2'), exitOnError=False),
        'Ln.PortableAppsDir'    : gv.Ln.VerifyPath(gv, rootDir.joinpath('PortableApps\PortableApps')),
        'Ln.PythonDir'          : gv.Ln.VerifyPath(gv, freeDir.joinpath('Pgm/WinPython-64bit-3.5.3.1Qt5/python-3.5.3.amd64')),
        'JAVA_HOME'             : gv.Ln.VerifyPath(gv, freeDir.joinpath('Pgm/Java/jdk1.8.0_66')),

        "Ln.PyGrep"              : '%Ln.PythonExe% ' + str(gv.Ln.VerifyPath(gv, gitRepoDir.joinpath("Scripts/python/LnPyGrep.zip"))),

        "Ln.WinScpKittyCmd"      : gv.Ln.VerifyPath(gv, gitRepoDir.joinpath("Scripts/python/Sources/KittyFromWinScp/bin/kitty-from-WinScp.cmd")),
        "Ln.WinScpKittyPy"       : gv.Ln.VerifyPath(gv, gitRepoDir.joinpath("Scripts/python/Sources/KittyFromWinScp/__main__.py")),
    }
    '''
