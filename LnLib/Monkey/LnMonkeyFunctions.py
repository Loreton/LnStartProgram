#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  aggiunge dei metodi alle classi di sistema
# updated by Loreto: 23-10-2017 14.38.53
# ######################################################################################
import shutil

from pathlib import Path
from time import strftime

from .. Common.LnLogger      import SetLogger

################################################
################################################
def LnPathCopy(self, target_filename, vSize=True, vMTime=False):
    assert self.is_file()
    logger = SetLogger(__name__) # log the caller
    '''
    alternative of Path.copy
    copyfile only if size or mtime ad differents
    params:
        target : target_filename
        vSize  : verify fileSize
        vMTime : verify mTime
    '''

    logger.info('working on files: {} - {}'.format(self, target_filename))
    target = Path(target_filename)
    diffSize, diffTime = False, False
    if target.exists():
        if vSize: # source != taget
            diffSize = (self.stat().st_size != target.stat().st_size)
        if vMTime: # source > taget
            diffTime = (self.stat().st_mtime > target.stat().st_mtime)

    logger.debug('diffTime value: {}'.format(diffTime))
    logger.debug('diffSize value: {}'.format(diffSize))

    if diffTime:
        logger.info('copying file...')
        shutil.copy(str(self), str(target))  # str() only there for Python < (3, 6)
    elif diffSize:
        logger.warning('DATETIME is equal but size is different... NOT copied')
    else:
        logger.info('DATETIME and SIZE are equals. copy skipped...')



######################################################
#
######################################################
def LnPathBackup(self, targetDir=None, logger=None):
    assert self.is_file()

    if not targetDir: targetDir = self.parent
    fname = '{NAME}_{DATE}{EXT}'.format(NAME=str(self.parent.name), DATE=strftime('%Y-%m-%d_%H_%M'), EXT=str(self.suffix))
    backupFile = Path(targetDir).joinpath(fname)
    backupFile = Path(backupFile)
    shutil.copy(str(self), str(backupFile))

# inseriamo i miei comandi nella classe Path.
Path.LnCopy   = LnPathCopy
Path.LnBackup = LnPathBackup