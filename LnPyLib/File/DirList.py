#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import os, fnmatch
import types


# from LnLib.Common.Exit          import Exit       as LnExit
from LnLib.Common.LnLogger      import SetLogger
# #########################################################################
# - dirList()
#   Return a list of file names found in directory 'dirName'
#       patternLIST: ["*.x", "*x*.y*", ...]
# #########################################################################
def DirList(topDir, patternLIST=['*'], onlyDir=False, maxDeep=99):
    logger  = SetLogger(package=__name__)

    # - eliminiamo i trailer BLANK
    patternLIST =  [x.strip() for x in patternLIST if x]

    LISTA = []
    for dirpath, dirs, files in os.walk(topDir, topdown=True):
        dirs[:] = [d for d in dirs if d != '.git'] # skip .git dirs
        depth = dirpath[len(topDir) + len(os.path.sep):].count(os.path.sep)

        if depth <= maxDeep:

            logger.debug('{DEPTH:02} - analyzing dir: {DIR}'.format(DEPTH=depth, DIR=dirpath))

            for file_pattern in patternLIST:
                if onlyDir: # se vogliamo solo le directory
                    if fnmatch.fnmatchcase(os.path.basename(dirpath), file_pattern):
                        if not dirpath in LISTA:
                            logger.debug("matched :{0}".format(dirpath) )
                            LISTA.append(dirpath)
                else:
                    LISTA.extend( [os.path.join(dirpath, filename) for filename in fnmatch.filter(files, file_pattern)] )


    return LISTA




