#
#  updated by Loreto: 17-10-2017 09.25.15
#

import os, sys
import subprocess
import pathlib as p         # dalla versione 3.4

import Functions as myFunc

class LnClass(): pass

def launchProgram(CMDList):
    logger.info(CMDList)
    procID = subprocess.Popen(CMDList, shell=False, universal_newlines=True)
    # print(procID)

    if True:
        name = input("press ENTER to continue....")




def setSUBST(drive, substDir):
    CMDList = []
    CMDList.append('subst')
    CMDList.append(drive)
    CMDList.append(substDir)
    launchProgram(CMDList)



#########################################################################
#
#########################################################################
def calculateMainDirs():
    # programName,  fAction, fConsole = args['program'], args['go'], args['console']

    logger.info("caller       : {}".format(args['caller']))
    logger.info("program      : {}".format(args['program']))
    logger.info("subst Drive  : {}".format(args['subst']))
    logger.info("action       : {}".format(args['go']))
    logger.info("console      : {}".format(args['console']))

        # - create dirs
    import pathlib
    scriptMain  = p.Path(sys.argv[0]).resolve()
    thisDir     = myFunc.VerifyPath(gv, scriptMain.parent)
    # print (type(scriptMain))
    # print (isinstance(scriptMain, pathlib.WindowsPath))
    # print (isinstance(scriptMain, pathlib.))

    sys.exit()
    thisDir   = myFunc.VerifyPath(gv, os.path.abspath(os.path.dirname(sys.argv[0])))
    thisDir   = myFunc.VerifyPath(gv, args['caller'].strip())

    logger.info("thisDir     : {}".format(thisDir))
    logger.info("")

    gv.Ln.Drive     = myFunc.VerifyPath(gv, thisDir[:2])
    gv.Ln.RootDir   = myFunc.VerifyPath(gv, os.path.abspath(os.path.dirname(thisDir)))
    gv.Ln.LoretoDir = myFunc.VerifyPath(gv, os.path.abspath(os.path.join(gv.Ln.RootDir, 'Loreto')))
    gv.Ln.FreeDir   = myFunc.VerifyPath(gv, os.path.abspath(os.path.join(gv.Ln.RootDir, 'LnFree')))
    gv.Ln.GitRepo   = myFunc.VerifyPath(gv, os.path.abspath(os.path.join(gv.Ln.RootDir, 'GIT-REPO')))

        # - logging
    logger.info("Drive       : {}".format(gv.Ln.Drive))
    logger.info("rootDir     : {}".format(gv.Ln.RootDir))
    logger.info("loretoDir   : {}".format(gv.Ln.LoretoDir))
    logger.info("LnFreeDir   : {}".format(gv.Ln.FreeDir))
    logger.info("LnGitRepo   : {}".format(gv.Ln.GitRepo))

        # --------------------------------------------
        # - se e' richiesto un drive SUBST ...
        # - impostiamo anche i path per quel drive
        # --------------------------------------------
    if args['subst']:
        substDrive = args['subst'].strip()
        if substDrive.lower() in ['x:', 'y:', 'w:', 'z:']:
            gv.subst.Drive = substDrive
            gv.subst.RootDir = gv.Ln.RootDir
            setSUBST(substDrive, gv.subst.RootDir )
            gv.subst.RootDir = substDrive
            gv.subst.LoretoDir = os.path.abspath(os.path.join(gv.subst.RootDir, 'Loreto'))
            gv.subst.LnFreeDir = os.path.abspath(os.path.join(gv.subst.RootDir, 'LnFree'))
            gv.subst.LnGitRepo = os.path.abspath(os.path.join(gv.subst.RootDir, 'GIT-REPO'))
                # - logging
            logger.info("subst Drive       : {}".format(gv.subst.Drive))
            logger.info("subst rootDir     : {}".format(gv.subst.RootDir))
            logger.info("subst loretoDir   : {}".format(gv.subst.LoretoDir))
            logger.info("subst LnFreeDir   : {}".format(gv.subst.LnFreeDir))
            logger.info("subst LnGitRepo   : {}".format(gv.subst.LnGitRepo))


# le variabili definite qui sono automaticamente globali.
if __name__ == '__main__':
    gv       = LnClass()
    gv.Ln    = LnClass()
    gv.myFunc  = myFunc
    gv.subst = LnClass()

    args   = myFunc.ParseInput() # ; print (args)
    logger = myFunc.LoggerSetUp(CONSOLE=args['console'])
    gv.logger = logger

    calculateMainDirs()




    if args['program'].lower().strip() in ['tc', 'totalcomander']:
        CMDList = myFunc.SetTotalCommander(gv)
        logger.info(CMDList)
