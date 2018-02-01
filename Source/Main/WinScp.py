#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
# updated by Loreto: 24-10-2017 14.24.47
# -----------------------------------------------
import os
import  platform
from pathlib import Path

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
def SetWinSCP(sectionVars):
    Ln     = Prj.LnLib
    gv      = Prj.gv
    C       = Ln.Color()

    logger = Ln.SetLogger(__name__)
    inpArgs = gv.args

    destServer = inpArgs['server']
    port       = inpArgs['port']

    if '@' in destServer:
        userName, server = destServer.split('@')
    else:
        server      = destServer
        userName    = os.getlogin()


    hostName, JBoossGuiPort, sshPort = Prj.getHostName(serverName=server, serverListFile=sectionVars.ServerListFile, exitOnNotFound=False)
    sessionName = hostName.split('.')[0]
    sectionName = 'Sessions\{}'.format(sessionName)

    # if userName: hostName = "{}@{}".format(userName, hostName)
    WINSCP_commandLIST = []

    extraSection                = {}
    extraSection[sectionName]    = {}
    sessID                   = extraSection[sectionName]
    sessID['HostName']       = hostName
    sessID['PortNumber']     = sshPort
    sessID['UserName']       = userName
    sessID['PingType']       = 2        # 1=...., 2=....
    sessID['PublicKeyFile']  = 'E:%5CLnDisk%5CLnFree%5CSecurity%5CMyKeys%5CLoreto%5CF602250_id_rsa.ppk'
    # sessID.ProxyMethod       = {PROXY_METHOD}
    # sessID.ProxyHost         = {PROXY_HOST}
    # sessID.ProxyPort         = 8081
    # sessID.ProxyUsername     = itacavdf
    sessID['FSProtocol']        = 0    # 0= SCP
    # sessID.RemoteDirectory   = {REMOTE_DIRECTORY}
    # sessID.UpdateDirectories = 0
    # sessID.Shell             = 'sudo%20su%20-'
    # sessID.ProxyDNS          = 2
    sessID['Color']             = 12379095



    # lettura del file ini
    iniFile = Ln.ReadIniFile(fileName=sectionVars.winScpINI, strict=False)
    iniFile.extraSections(extraSection)
    iniFile.read(resolveEnvVars=False)
    serverList = Ln.Dict(iniFile.dict)
    serverList.printTree(fPAUSE=True)




    WINSCP_commandLIST.append(sectionVars.winScpEXE)
    iniFile = Path(sectionVars.winScpINI).resolve()
    if inpArgs['new_instance']:
        WINSCP_commandLIST.append('/newinstance')
    WINSCP_commandLIST.append('/ini={}'.format(str(iniFile)))

    if 'privateKey' in sectionVars:
        privateKeyFile = Path(sectionVars.privateKey).resolve()
        WINSCP_commandLIST.append('/privatekey={}'.format(str(privateKeyFile)))

    WINSCP_commandLIST.append('/sessionname={}'.format(sessionName.upper()))
    WINSCP_commandLIST.append(sessionName)
    print ()
    for item in WINSCP_commandLIST:
        C.printColored(color=C.yellowH, text=item, tab=4)
    print ()


    return WINSCP_commandLIST



##############################################
# Creare una session like this....
# E:\LnED\Lacie232\Filu\LnDisk\LnFree\Network\FTPc\WinSCP\winscp.exe
#   /newinstance
#   /ini=E:\LnED\Lacie232\Filu\LnDisk\LnFree\Network\FTPc\WinSCP\Ln_ini\WinSCP_Dynamic.ini
#   /privatekey=E:\LnED\Lacie232\Filu\LnDisk\LnFree\Security\MyKeys\myRoot\myRoot_id.rsa
#   /sessionname=SEFALL22
#   scp://f602250@SEFALL22.utenze.bankit.it
##############################################
def SetWinSCP_rawsetting(sectionVars):
    Ln     = Prj.LnLib
    gv      = Prj.gv
    C       = Ln.Color()

    logger = Ln.SetLogger(__name__)
    inpArgs = gv.args

    destServer = inpArgs['server']
    port       = inpArgs['port']

    if '@' in destServer:
        userName, server = destServer.split('@')
    else:
        server      = destServer
        userName    = os.getlogin()

    # serverListFile=sectionVars.ServerListFile
    # sectionVars.printTree(fPAUSE=True)
    hostName, JBoossGuiPort, sshPort = Prj.getHostName(serverName=server, serverListFile=sectionVars.ServerListFile, exitOnNotFound=False)
    sessionName = hostName.split('.')[0]

    if userName: hostName = "{}@{}".format(userName, hostName)

    WINSCP_commandLIST = []

    '''
        # non funzionano....
    WINSCP_commandLIST.append('/rawconfig')
    WINSCP_commandLIST.append('/username={}'.format(userName))
    WINSCP_commandLIST.append('/rawsettings "/username={}"'.format(userName))
    WINSCP_commandLIST.append('/log=D:\zTemp\WinSCP.log')
    WINSCP_commandLIST.append('/loglevel=2') # [0..2]

    # WINSCP_commandLIST.append('/log="D:\tmp\WinSCP.log"')

    WINSCP_commandLIST.append('/rawsettings username=loreto')
        [/rawsettings setting1=value1 setting2=value2 ...]
    '''

    # - NON mettere i doppi apici sui parametri...
    WINSCP_commandLIST.append(sectionVars.winScpEXE)
    iniFile = Path(sectionVars.winScpINI).resolve()
    if inpArgs['new_instance']:
        WINSCP_commandLIST.append('/newinstance')
    WINSCP_commandLIST.append('/ini={}'.format(str(iniFile)))

    if 'privateKey' in sectionVars:
        privateKeyFile = Path(sectionVars.privateKey).resolve()
        WINSCP_commandLIST.append('/privatekey={}'.format(str(privateKeyFile)))

    WINSCP_commandLIST.append('/sessionname={}'.format(sessionName.upper()))
    WINSCP_commandLIST.append('scp://{}'.format(hostName))
    print ()
    for item in WINSCP_commandLIST:
        C.printColored(color=C.yellowH, text=item, tab=4)
    print ()

    return WINSCP_commandLIST
