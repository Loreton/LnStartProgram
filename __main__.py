#
#  updated by Loreto: 19-10-2017 15.58.40
#

# import  os, sys

# from    pathlib import *         # dalla versione 3.4
# import  pathlib as p         # dalla versione 3.4
# from    time import sleep

import  Functions as myFunc

# class LnClass(): pass






# le variabili definite qui sono automaticamente globali.
if __name__ == '__main__':
    gv        = myFunc.LnClass()
    gv.env    = myFunc.LnClass()
    gv.Ln     = myFunc


    args   = gv.Ln.ParseInput() # ; print (args)
    gv.fDEBUG = args['debug']
    logger = gv.Ln.InitLogger(fFILE=args['log_file'], fCONSOLE=args['log_console'], ARGS=args)
    gv.logger = logger

    gv.Ln.CalculateMainDirs(gv, args)
    gv.Ln.SetEnvVars(gv)


    if args['program'].lower().strip() in ['tc', 'totalcomander']:
        CMDList = gv.Ln.SetTotalCommander(gv)
        gv.Ln.LaunchProgram(gv, 'TotalCommander command list:', CMDList)