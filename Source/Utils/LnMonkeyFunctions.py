#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  aggiunge dei metodi alle classi di sistema
# updated by Loreto: 23-10-2017 14.38.53
# ######################################################################################
import sys
import shutil

from pathlib import Path, WindowsPath
from time import strftime

from . LnKeyboard import keyb_input



################################################
################################################
def LnPathCopy(source, target, logger):
    #assert Path(source).is_file()
    '''
    alternative of Path.copy
    copyfile only if size or mtime ad differents
    params:
        target : target
        vSize  : verify fileSize
        vMTime : verify mTime
    '''

    logger.info('working on files: {} - {}'.format(source, target))
    target = Path(target)
    diffSize, diffTime = False, False
    src = source.stat()
    tgt = src # default nel caso target non esista.
    if target.exists():
        tgt = target.stat()
        diffSize = (src.st_size != tgt.st_size)
        diffTime = (src.st_mtime > tgt.st_mtime)

    logger.info('diffTime value: {0} <--> {1}'.format(src.st_mtime, tgt.st_mtime))
    logger.info('diffSize value: {0} <--> {1}'.format(src.st_size, tgt.st_size))

    if diffTime:
        logger.info('copying file...')
        shutil.copy(str(source), str(target))  # str() only there for Python < (3, 6)
    elif diffSize:
        logger.warning('same DATETIME but different SIZE... NOT copied')
    else:
        logger.info('DATETIME and SIZE are equals. copy skipped...')



######################################################
#
######################################################
def LnPathBackup(source, targetDir=None, logger=None):
    assert source.is_file()

    if not targetDir: targetDir = source.parent
    fname = '{NAME}_{DATE}{EXT}'.format(NAME=str(source.parent.name), DATE=strftime('%Y-%m-%d_%H_%M'), EXT=str(source.suffix))
    backupFile = Path(targetDir).joinpath(fname)
    backupFile = Path(backupFile)
    shutil.copy(str(source), str(backupFile))



######################################################
#
######################################################
def checkPath(_path, errorOnPathNotFound=False):
    if isinstance(_path, (WindowsPath, str)):
        if _path[1] == ':':
            _path = Path(_path).resolve() # absolute path and cut  \\\\ excedents
            if not _path.exists():
                if errorOnPathNotFound:
                    print('\n    {_path} path NOT FOUND. Pls change the config file.\n'.format(**locals()))
                    sys.exit(1)
                else:
                    choice=keyb_input('\n   {_path} file NOT FOUND. [I]gnore'.format(**locals()), validKeys='i|I')
        _path = str(_path)
    return _path


# inseriamo i miei comandi nella classe Path.
Path.LnCopy   = LnPathCopy
Path.LnBackup = LnPathBackup
Path.LnVerify = checkPath