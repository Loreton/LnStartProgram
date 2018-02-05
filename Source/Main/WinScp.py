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
    inpArgs = Ln.Dict(gv.args)

    logger     = Ln.SetLogger(__name__)

    destServer = inpArgs.server
    port       = inpArgs.port

    if '@' in destServer:
        userName, server = destServer.split('@')
    else:
        server      = destServer
        userName    = os.getlogin()

    if inpArgs.firstPosParameter == 'winscp_loreto':
        winscpIniFname = str(Path(sectionVars['winScp_loreto_INI']).resolve())
    else:
        winscpIniFname = str(Path(sectionVars['winScp_bdi_INI']).resolve())

    hostName, JBoossGuiPort, sshPort = Prj.getHostName(serverName=server, serverListFile=sectionVars.ServerListFile, exitOnNotFound=False)


    # - create winscp command[]
    WINSCP_commandLIST = []
    WINSCP_commandLIST.append(sectionVars.winScpEXE)


    myKey = 'privateKey.{}'.format(userName)
    '''
        privateKey.root     = ${VARS:Ln_FreeDir}\Security\MyKeys\myRoot\myRoot_id.rsa.ppk
        privateKey.f602250  = ${VARS:Ln_FreeDir}\Security\MyKeys\Loreto\F602250_id_rsa.ppk
    '''
    if myKey in sectionVars:
        privateKeyFile = Path(sectionVars[myKey]).resolve()
        # WINSCP_commandLIST.append('/privatekey={}'.format(str(privateKeyFile)))
    else:
        privateKeyFile = None


        # read winscp.ini file
    winscpIni  = Ln.ReadIniFile(fileName=winscpIniFname, kvDelimiters=['='], strict=True)
    winscpDict = winscpIni.toDict(dictType=Ln.Dict)


    # Section Samples:
    #   [Sessions\Domestic/Osiride2/osi2-phys-601]
    #   [Sessions\JBoss_WF2/Sterope/WEFALF49%20-%20Collaudo]

    sessionName = hostName.split('.')[0]            # name of winscp SESSION TAB


    EXISTS = False
    C.printColored(color=C.cyanH, text='searching for session: {}'.format(sessionName), tab=4)

    for section in winscpDict.keys():
        if section.startswith('Sessions\\'):
            sectionToken = section.lower().replace('/', ' ').replace('\\', ' ').replace ('%20', ' ').split()
            if sessionName in sectionToken:
                C.printColored(color=C.cyanH, text='FOUND: {}'.format(section), tab=4)
                EXISTS = True
                sessionName = section.split('Sessions\\')[1] # prendo il nome della section attuale....
                # token = sessionName.replace('/', ' ').replace('\\', ' ').replace ('%20', ' ').split()
                displaySessName = section.rsplit('/', 1)[1].replace('%20', '.').replace('.-.', '-')
                # if len(token) > 1:
                #     displaySessName = '.'.join(token[-2:]) # last two qulifiers
                # else:
                #     displaySessName = '.'.join(token) # all (one) qulifiers
                break



    if EXISTS:
        sectionName = section
    else:
        sessionName = '{}.{}'.format(hostName.split('.')[0], userName)  # hostname.ussername
        sectionName = 'Sessions\{}'.format(sessionName)


        # creiamo la section con i nostri parametri
    mySection              = {}
    mySection[sectionName] = {}
    sectID                 = mySection[sectionName]
    sectID['HostName']     = hostName
    sectID['PortNumber']   = sshPort
    sectID['UserName']     = userName
    sectID['PingType']     = 2        # 1           = ...., 2 = ....
    sectID['FSProtocol']   = 0    # 0               = SCP
    sectID['Color']        = 12379095

    if privateKeyFile:
        sectID['PublicKeyFile']   = str(privateKeyFile)

    if userName == 'root':
        sectID['RemoteDirectory'] = '/root'
    else:
        sectID['RemoteDirectory'] = '/home/{}'.format(userName)

    # sectID.ProxyMethod       = {PROXY_METHOD}
    # sectID.ProxyHost         = {PROXY_HOST}
    # sectID.ProxyPort         = 8081
    # sectID.ProxyUsername     = itacavdf
    # sectID.UpdateDirectories = 0
    # sectID.Shell             = 'sudo%20su%20-'
    # sectID.ProxyDNS          = 2

        # inject mySection
    winscpDict = winscpIni.updateSection(mySection)
    if gv.fDEBUG: winscpDict[section].printTree(fPAUSE=True)
        # save new config data
    winscpIni.updateFile(replace=True, backup=True)


    WINSCP_commandLIST.append(sessionName)

    WINSCP_commandLIST.append('/ini={}'.format(winscpIniFname))
    WINSCP_commandLIST.append('/log={}'.format('D:/temp/winscp.log'))
    if inpArgs['new_instance']:
        WINSCP_commandLIST.append('/newinstance')

    WINSCP_commandLIST.append('/sessionname={}'.format(displaySessName.upper()))
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
