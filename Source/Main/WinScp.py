#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
# updated by Loreto: 24-10-2017 14.24.47
# -----------------------------------------------
import os
import  platform

import Source as Prj


##############################################
# Creare una session like this....
#   [Sessions\JBossInfra/SEFALD93]
#   HostName=SEFALD93.utenze.bankit.it
#   UserName=root
#   FSProtocol=0            --> 0 = SCP
#   LocalDirectory=D:%5Ctmp
#   RemoteDirectory=/tmp
#   Shell=sudo%20/bin/su%20-%20jboss   --> (se serve) - solo per scp
#   Color=12379095
##############################################
def SetWinScp(sectionVars):
    Ln     = Prj.LnLib
    logger = Ln.SetLogger(__name__)
    gv      = Prj.gv
    inpArgs = Prj.gv.args

    destServer = Prj.gv.args['destServer']
    port        = Prj.gv.args['destPort']

    CMDList = []

    if '@' in destServer:
        userName, serverName = destServer.split('@')
    else:
        serverNamw  = destServer
        userName    = os.getlogin()


    mySession = """
        [Sessions\Dynamic/{SESSION_NAME}]
        HostName={HOST}
        PortNumber={PORT}
        UserName={USER}
        PingType=2
        PublicKeyFile={PUB_KEY}
        ProxyMethod={PROXY_METHOD}
        ProxyHost={PROXY_HOST}
        ProxyPort=8081
        ProxyUsername=itacavdf
        FSProtocol=0
        RemoteDirectory={REMOTE_DIRECTORY}
        UpdateDirectories=0
        Shell={SHELL}
        ProxyDNS=2
        Color=12379095
        """.format( SESSION_NAME=serverName,
                    HOST=serverName,
                    PORT=port,
                    USER=userName,
                    PUB_KEY='E:%5CLnDisk%5CLnFree%5CSecurity%5CMyKeys%5CLoreto%5CF602250_id_rsa.ppk',
                    PROXY_METHOD=2, # capire 2, 3 o altro
                    PROXY_HOST='itaca-prod.utenze.bankit.it',
                    PROXY_PORT='8081',
                    PROXY_USER='xxxx',
                    FSPROTOCOL=0,     # 0= SCP
                    PINGTYPE=1,     # 1=...., 2=....
                    REMOTE_DIRECTORY='/home/pi',
                    SHELL='sudo%20su%20-',
                )


        # -------------------------------------------------
        # - Setting delle variabili
        # -------------------------------------------------
    for varName, varValue in sectionVars.items():
        if varName.startswith('opt.'):
            varName = varName[4:]
            fMANDATORY = False
        else:
            fMANDATORY = True

        # salviamolo in formato Path
        sectionVars[varName] = Ln.VerifyPath(varValue, exitOnError=fMANDATORY)
        Ln.OsEnv.setVar(varName, sectionVars[varName])
        if varName.lower() == 'workingdir':
            os.chdir(str(sectionVars[varName]))


    OSbits = platform.architecture()[0]
    logger.info( "Stiamo lavorando con TotalCommander {}".format(OSbits))
    if OSbits.lower() == "64bit":
        TCexe = Ln.VerifyPath(sectionVars.Ln_TC_Dir.joinpath('realApp/WinCmd/TOTALCMD64.exe'))
    else:
        TCexe = Ln.VerifyPath(sectionVars.Ln_TC_Dir.joinpath('realApp/WinCmd/TOTALCMD.exe'))

    if fDEBUG: sectionVars.printTree("IniVars variables", fPAUSE=True)

    CMDList.append(TCexe)
    CMDList.append('/I={}'.format(sectionVars.Ln_TC_IniFile))
    CMDList.append('/F={}'.format(sectionVars.Ln_TC_ftpIniFile))

    return CMDList

'''
##############################################
# Creare una session like this....
#   [Sessions\JBossInfra/SEFALD93]
#   HostName=SEFALD93.utenze.bankit.it
#   UserName=root
#   FSProtocol=0            --> 0 = SCP
#   LocalDirectory=D:%5Ctmp
#   RemoteDirectory=/tmp
#   Shell=sudo%20/bin/su%20-%20jboss   --> (se serve) - solo per scp
#   Color=12379095
##############################################
def PrepareWinScpSession(gv):
    serverName = gv.INPUT_PARAM.serverName

    if '@' in serverName:
        userName, server = serverName.split('@')
    else:
        server      = serverName
        userName    = os.getlogin()

    iniFile = gv.Ln.ReadIniFile(gv.INPUT_PARAM.iniFile, strict=False, subSectionChar=['\\', '/'], resolveEnvars=False)
    iniFile.Delimiters('=')
    iniFile.read()
    gv.winscpINI = gv.Ln.LnDict(iniFile.dict)

    gv.winscpINI.Sessions.JBossInfra.printTree(fEXIT=True)
    # for key in gv.winscpINI.Sessions.Infra.keys():
        # print (key)

    sys.exit()

    sudoJBOSS                 = 'sudo%20/bin/su%20-%20jboss'
    mySession.HostName        = server
    mySession.UserName        = userName
    mySession.FSProtocol      = 0                   #--> 0 = SCP
    mySession.LocalDirectory  = 'D:%5Ctmp'
    mySession.RemoteDirectory = '/tmp'
    mySession.Shell           = sudoJBOSS
    mySession.Color           = 12379095

    mySession = """
        [Sessions\Dynamic/{SESSION_NAME}]
        HostName={HOST}
        PortNumber={PORT}
        UserName={USER}
        PingType=2
        PublicKeyFile={PUB_KEY}
        ProxyMethod={PROXY_METHOD}
        ProxyHost={PROXY_HOST}
        ProxyPort=8081
        ProxyUsername=itacavdf
        FSProtocol=0
        RemoteDirectory={REMOTE_DIRECTORY}
        UpdateDirectories=0
        Shell={SHELL}
        ProxyDNS=2
        Color=12379095
    """.format( SESSION_NAME='dynamicSession',
                HOST='',
                PORT='8023',
                USER='',
                PUB_KEY='E:%5CLnDisk%5CLnFree%5CSecurity%5CMyKeys%5CLoreto%5CF602250_id_rsa.ppk',
                PROXY_METHOD=2, # capire 2, 3 o altro
                PROXY_HOST='itaca-prod.utenze.bankit.it',
                PROXY_PORT='8081',
                PROXY_USER='xxxx',
                FSPROTOCOL=0,     # 0= SCP
                PINGTYPE=1,     # 1=...., 2=....
                REMOTE_DIRECTORY='/home/pi',
                SHELL='sudo%20su%20-',
            )


    # hostName, dummy01, dummy02 = gv.Prj.HostNames(gv, server, exitOnNotFound=False)
    # sessionName = hostName.split('.')[0]

    # if userName: hostName = "{}@{}".format(userName, hostName)


    # os.chdir(gv.ini.VARS.winscpDIR)

    CMDList = []

    # - NON mettere i doppi apici sui parametri...
    WINSCP_commandLIST.append(gv.ini.VARS.winscpEXE)
    WINSCP_commandLIST.append('/ini={}'.format(gv.ini.VARS.winscpINI))
    if 'privateKey' in gv.ini.VARS:
        WINSCP_commandLIST.append('/privatekey={}'.format(gv.ini.VARS.privateKey))
    WINSCP_commandLIST.append('/sessionname={}'.format(sessionName.upper()))
    WINSCP_commandLIST.append('scp://{}'.format(hostName))
    print(WINSCP_commandLIST)
    return WINSCP_commandLIST

'''