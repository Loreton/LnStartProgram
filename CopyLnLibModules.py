#!/opt/python3.4/bin/python3.4

import sys
import os
import shutil
import time
from pathlib import Path


def baseLnLibFiles():
    files = []

                # SubDir,                  FileSource,               fileDest
    # basic  modules
    files.append(['',                    '__init__LnLib.py',            '__init__.py' ])
    files.append(['',                    'LnCreate_zip.sh',            '=' ])

    files.append(['Common',              'Exit.py',                     '=' ])
    files.append(['Common',              'LnColor.py',                  '=' ])
    files.append(['Common',              'LnLogger.py',                 '=' ])

    files.append(['Common/colorama',     '__init__.py',                 '=' ])
    files.append(['Common/colorama',     'ansi.py',                     '=' ])
    files.append(['Common/colorama',     'ansitowin32.py',              '=' ])
    files.append(['Common/colorama',     'initialise.py',               '=' ])
    files.append(['Common/colorama',     'win32.py',                    '=' ])
    files.append(['Common/colorama',     'winterm.py',                  '=' ])

    files.append(['Dict',                '__init__.py',                 '=' ])
    files.append(['Dict',                'DictToList.py',               '=' ])
    files.append(['Dict',                'Ln_DotMap.py',                '=' ])
    files.append(['Dict',                'PrintDictionaryTree.py',      '=' ])

    files.append(['File',                '__init__.py',                 '=' ])
    files.append(['File',                'DirList.py',                  '=' ])
    files.append(['File',                'ReadIniFile_Class.py',        '=' ])
    files.append(['File',                'ReadWriteTextFile.py',        '=' ])

    files.append(['ParseInput',          '__init__.py',                 '=' ])
    files.append(['ParseInput',          'check_file.py',               '=' ])
    files.append(['ParseInput',          'ColoredHelp.py',              '=' ])
    files.append(['ParseInput',          'CreateParser.py',             '=' ])
    files.append(['ParseInput',          'Debug_Options.py',            '=' ])
    files.append(['ParseInput',          'IniFile_Options.py',          '=' ])
    files.append(['ParseInput',          'Log_Options.py',              '=' ])
    files.append(['ParseInput',          'MainParseInput.py',           '=' ])
    files.append(['ParseInput',          'PositionalParameters.py',     '=' ])

    files.append(['Process',             '__init__.py',                 '=' ])
    files.append(['Process',             'ExecRcode.py',                '=' ])
    files.append(['Process',             'RunProgram.py',               '=' ])

    files.append(['System',              '__init__.py',                 '=' ])
    files.append(['System',              'GetKeyboardInput.py',         '=' ])
    files.append(['System',              'GlobalVars.py',               '=' ])

    # project specific modules
    files.append(['File',                'VerifyPath.py',               '=' ])
    files.append(['Monkey',              'LnMonkeyFunctions.py',        '=' ])
    files.append(['System',              'SetOsEnv.py',                 '=' ])

    return files

##################################################
#
##################################################
def copyFile(sourceFileName, destFileName, chmod=None):
    print ('    copying...{0:<60} --> {1}'.format( sourceFileName, destFileName))
    try:
        destdir = os.path.dirname(destFileName)
        srcdir  = os.path.dirname(sourceFileName)
        if Action:
            if not os.path.exists(destdir):
                os.makedirs(destdir)
                shutil.copystat(srcdir, destdir)
            shutil.copy2(sourceFileName, destFileName)  # preserve metadata
            if chmod:
                # print ('changing mode.....')
                os.chmod(destFileName, chmod)


    except (IOError, os.error) as why:
        msg = "Can't COPY [{0}] to [{1}]: {2}".format(sourceFileName, destFileName, str(why))
        print ()
        print (msg)
        print ()


##################################################
#
##################################################
def processFiles(srcDir, dstDir, files):
    '''
        srcDir: LnPythonLib source directory
        dstDir: LnLib directory in Project direcotry
        files[[],[],..]: files to be copied
    '''
    for fname in files:
        subDir, srcFname, dstFname = fname
        if dstFname == '=': dstFname = srcFname
        sourceFileName  = Path(srcDir / subDir / srcFname)
        destFileName    = Path(dstDir / subDir / dstFname)

        if not Path(sourceFileName).exists():
            print ('    {SFILE:<50} ... non esiste.'.format(SFILE=str(sourceFileName)))
            sys.exit(1)

        outputFormat="%Y/%m/%d %H:%M:%S"
        relativeName = str(destFileName).split(str(prjDir))[1][1:]
        relativeName = Path(subDir) / srcFname

        if not destFileName.exists():
            copyFile(str(sourceFileName), str(destFileName), chmod=0o400)

        else:
            sourceSECs   = os.stat(str(sourceFileName)).st_mtime      # modification time in secondi
            Tuple       = time.localtime(sourceSECs)
            sourceSTR   = time.strftime(outputFormat, Tuple)

            destSECs     = os.stat(str(destFileName)).st_mtime        # modification time in secondi
            Tuple       = time.localtime(destSECs)
            destSTR     = time.strftime(outputFormat, Tuple)


            if sourceSECs > destSECs:
                copyFile(str(sourceFileName), str(destFileName), chmod=0o400)

            elif sourceSECs < destSECs and ReverseCopy:
                copyFile(str(destFileName), str(sourceFileName))

            elif sourceSECs == destSECs:
                pass

            else:
                print ('''    {FILE:<50} ... destination file is newer than source ([--rc] option for reverseCopy
                                    SOURCE.: {SDATE}
                                    DEST...: {DDATE}'''.format(FILE=str(relativeName), SDATE=sourceSTR, DDATE=destSTR))


################################################################################
# - M A I N
################################################################################
if __name__ == "__main__":
    global Action, ReverseCopy

        # ------------------------------------------
        # - Preparazione directories
        # ------------------------------------------
    prjDir  = Path(sys.argv[0]).resolve().parent
    prjDir  = Path(sys.argv[0]).resolve().parent

    if not prjDir.is_dir():
        msg = "La directory di progetto [{0}] non esiste.".format(prjDir)
        print ()
        print (msg)
        print ()
        sys.exit(1)

    LnPythonLibDir  = Path(sys.argv[0]).resolve().parent.parent / 'LnPythonLib'
    if not LnPythonLibDir.is_dir():
        msg = "La directory LnPythonLib [{0}] non esiste.".format(prjDir)
        print ()
        print (msg)
        print ()
        sys.exit(1)

    # LnPythonLibDir.exists()
    prjName = prjDir.name
    destDir = prjDir / 'LnLib'
    print ( )
    print ('    projectNAme...:',    prjName)
    print ('    LnPythonLib...:',    LnPythonLibDir)
    print ('    projectDir....:',    prjDir)
    print ('    destinationDir:',    destDir)
    print ( )

    try:
        Action = sys.argv[1]
        Action = True if Action.lower() == '--go' else False
    except:
        Action = False

    try:
        ReverseCopy = sys.argv[2]
        ReverseCopy = True if ReverseCopy.lower() == '--rc' else False
    except:
        ReverseCopy = False

    processFiles(LnPythonLibDir, destDir, baseLnLibFiles())

    if not Action:
        print ()
        print ('immettere il parametro --go per eseguire la copia...')
        print ('immettere il parametro --go per eseguire la copia...')
        print ()