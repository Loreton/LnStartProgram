#!/usr/bin/python
# -*- coding: utf-8 -*-
# .................-*- coding: latin-1 -*-
# ................-*- coding: iso-8859-15 -*-
#!/usr/bin/python -O

import sys
import Source as Prj

########################################################
# Ricerca di un nome
########################################################
def getHostName(serverName, serverListFile, exitOnNotFound=False):
    Ln     = Prj.LnLib
    gv     = Prj.gv


    logger = Ln.SetLogger(__name__)
    C      = Ln.Color()

        # cerchiamo il server richiesto...
    serverFOUND = None



    logger.info ('going to read file....: {}'.format(serverListFile))
    iniFile    = Ln.ReadIniFile(serverListFile, strict=True)
    serverList = iniFile.toDict(dictType=Ln.Dict)
    C.printColored(color=C.yellowH, text='searching for server...: {}'.format(serverName), tab=4)

    SECTIONS = []
    for sectName in serverList:
        if sectName.startswith('Server.'):
            SECTIONS.append(sectName)


    serverNameLOWER = serverName.lower()
    for sectName in SECTIONS:
        if serverFOUND:
            logger.info ('FOUND....: {}'.format( serverFOUND))
            break

        logger.debug('section...: {:<20} - searching for server: {}'.format(sectName, serverNameLOWER))

        sectionID = serverList[sectName]

            #  ... sia la key (alias name) che il proimo qulificatore dell'itemn
        for serverAlias, serverData in sectionID.items():
            logger.info('alias...: {:<20} - realName: {}'.format(serverAlias, serverData))
            serverReal = serverData.split(',', 1)[0].strip()
            if serverNameLOWER in [serverAlias.lower(), serverReal.lower()]:
                serverFOUND = serverData
                break



    if serverFOUND:
            # assegnazione valori
        data = [x.strip() for x in serverFOUND.split(',')]
        logger.info("serverFOUND: {}".format(data))
        C.printColored(color=C.yellowH, text='server FOUND...: {}'.format(data), tab=4)
        server, guiport, sshport = data

        return server, guiport, sshport

    elif exitOnNotFound:
        print()
        C.printRedH  ('     {SERVERNAME} - is unknown'.format(SERVERNAME=serverName))
        print()
        Ln.Exit(1002)

    else:
        ''' tentiamo di individuare il dominio...'''
        C.printColored(color=C.yellowH, text='server NOT found in serverList, trying anyway...', tab=4)
        if not '.' in serverName:
            namePrefix = serverName.lower()[:5]
            sectPtr = serverList['MAIN']
            defDomain = serverList['MAIN']['DEFALT_DOMAIN']

            for domain, val in serverList['MAIN'].items():
                if namePrefix in val.split('.'):
                    defDomain = domain
                    break


            serverName += '.{}'.format(defDomain)

        C.printColored(color=C.yellowH, text='returning server: {}'.format(serverName), tab=4)

        return serverName, 9990, 22   # cont default port value

    return None, None, None
