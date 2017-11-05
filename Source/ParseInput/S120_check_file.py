#
from pathlib import Path
from LnLib.Common.Exit     import Exit      as LnExit
from LnLib.Common.LnColor  import LnColor
C = LnColor()
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

