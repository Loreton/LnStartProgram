from . S110_MyHelp import myHELP

#######################################################
# LOG options
#######################################################
def logParameters(myParser, gVar, required=False):
    logGroup = myParser.add_mutually_exclusive_group(required=False)  # True indica obbligatorietà di uno del gruppo
    myParser.add_argument('---------------log-options ----',
                                required=False,
                                action='store_true',
                                help=myHELP('', None))

        # log debug su console
    logGroup.add_argument( "--log-console",
                                metavar='',
                                required=False,
                                default=False,
                                nargs='*',
                                help=myHELP("""attivazione log sulla console.
    E' possibile indicare una o più stringhe
    per identificare le funzioni che si vogliono inserire nel log.
    Possono essere anche porzioni di funcName separate da ' ' Es: pippo pluto ciao""", False))

        # log debug su file
    logGroup.add_argument('--log',
                                metavar='',
                                required=False,
                                default=False,
                                nargs='*',
                                help=myHELP("""attivazione log sul file.
    E' possibile indicare una o più stringhe
    per identificare le funzioni che si vogliono inserire nel log.
    Possono essere anche porzioni di funcName separate da ' ' Es: pippo pluto ciao
    verra' utilizzao il file di log definito tramite --log-filename.""", False))


        # definizione file di log
    myParser.add_argument('--log-filename',
                                metavar='',
                                # str=_fileCheck,
                                required=False,
                                default=gVar.defaultLogFile,
                                help=myHELP('Specifies log fileName...', gVar.defaultLogFile))





####################################
# # _fileCheck()
####################################
def _fileCheck(fileName):
    fileName = fileName.strip().strip("'").strip()

    try:
        fileName = Path(fileName).resolve()     # strict=True dalla 3.6

    except Exception as why:
        print()
        print (str(why))
        # LnColor.printYellow ('  {FILE} is not a valid file...'.format(FILE=fileName) + LnColor.RESET)
        print()
        sysExit()

    return fileName

