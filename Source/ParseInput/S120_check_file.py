
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
        print (str(why))
        # LnColor.printYellow ('  {FILE} is not a valid file...'.format(FILE=fileName) + LnColor.RESET)
        print()
        sysExit()

    return fileName

