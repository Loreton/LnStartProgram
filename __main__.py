#
#  updated by Loreto: 20-10-2017 14.59.18
#

import  Functions as Prj
import  LnLib as Ln

#@TODO: spostare le directory su un file di configurazione
#@TODO: preparare per Executor

if __name__ == '__main__':
    # gv        = myFunc.LnClass() # definita nell __init__.py
    # gv.env    = myFunc.LnClass()
    gv        = Ln.LnDict()
    gv.env    = Ln.LnDict()
    gv.prj    = Prj
    gv.Ln     = Ln


    args      = gv.prj.ParseInput() # ; print (args)
    gv.args   = Ln.LnDict(args)
    gv.fDEBUG = gv.args.debug
    logger    = gv.prj.InitLogger(fFILE=gv.args.log_file, fCONSOLE=gv.args.log_console, ARGS=args)
    gv.logger = logger

    gv.prj.CalculateMainDirs(gv, args)
    gv.prj.SetEnvVars(gv)


    if args['program'].lower().strip() in ['tc', 'totalcomander']:
        CMDList = gv.prj.SetTotalCommander(gv)
        gv.prj.LaunchProgram(gv, 'TotalCommander command list:', CMDList)