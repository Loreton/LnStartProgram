#
# updated by ...: Loreto Notarantonio
# Version ......: 05-02-2018 17.01.56
#
from pathlib import Path
import sys
from  ... Common.LnColor import LnColor; C=LnColor()
from  ... Common.Exit    import Exit as LnExit
#
####################################
# # _fileCheck()
####################################
def check_file(fileName):
    fileName = fileName.strip().strip("'").strip()

    fileName = Path(fileName)     # strict=True dalla 3.6
    if fileName.is_file():
        return str(fileName.resolve())
    else:
        C.printColored(color=C.yellow, text='file NOT FOUND: {FILE}'.format(FILE=str(fileName)), tab=4)
        sys.exit(1)

        # LnExit non funziona bene....
        # LnExit(1, 'exiting... analysing file: {FILE}'.format(FILE=str(fileName)))

    '''
    try:
        fileName = Path(fileName).resolve()     # strict=True dalla 3.6

    except Exception as why:
        print()
        C.printColored(color=C.yellow, text=str(why), tab=4)
        print()
        LnExit(1, 'exiting... analysing file: {FILE}'.format(FILE=str(fileName)))


    return fileName
    '''

