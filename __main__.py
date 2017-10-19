#
#  updated by Loreto: 19-10-2017 16.51.29
#

import  Functions as myFunc

#@TODO: spostare le directory su un file di configurazione
#@TODO: preparare per Executor

if __name__ == '__main__':
    gv        = myFunc.LnClass() # definita nell __init__.py
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