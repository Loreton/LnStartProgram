#
# updated by ...: Loreto Notarantonio
# Version ......: 03-01-2018 10.14.39
#
from pathlib import Path

from  ... Common.LnColor import LnColor; C=LnColor()
from  ... Common.Exit    import Exit as LnExit
#
####################################
# # _fileCheck()
####################################
def check_file(fileName):
    fileName = fileName.strip().strip("'").strip()

    try:
        fileName = Path(fileName).resolve()     # strict=True dalla 3.6

    except Exception as why:
        print()
        C.printColored(color=C.yellow, text=str(why), tab=4)
        print()
        LnExit(1, 'exiting... analysing file: {FILE}'.format(FILE=fileName))


    return fileName

