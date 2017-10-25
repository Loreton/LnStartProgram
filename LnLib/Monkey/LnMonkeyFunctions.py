#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  aggiunge dei metodi alle classi di sistema
# updated by Loreto: 23-10-2017 14.38.53
# ######################################################################################

from pathlib import Path, PurePath
from time import strftime

################################################
# sostituisce la Path.copy  con la mia
# Copia solo se size diverso e se mtime diverso
################################################
import shutil
def LnPathCopy(self, target, vSize=True, vMTime=False, logger=None):
    assert self.is_file()

    target = Path(target)
    if target.exists():
        diff  = 0
        if vSize:
            diff += not (self.stat().st_size == target.stat().st_size)
        if vMTime:
            diff += not (self.stat().st_mtime == target.stat().st_mtime)
    else:
        diff  = 1


    if diff:
        if logger: logger.info('copying....: {} --> {}'.format(self, target))
        shutil.copy(str(self), str(target))  # str() only there for Python < (3, 6)
    else:
        if logger: logger.info('copy skipped for: {} --> {}'.format(self, target))



######################################################
#
######################################################
def LnPathBackup(self, targetDir=None, logger=None):
    import shutil
    assert self.is_file()

    if not targetDir: targetDir = self.parent
    fname = '{NAME}_{DATE}{EXT}'.format(NAME=str(self.parent.name), DATE=strftime('%Y-%m-%d_%H_%M'), EXT=str(self.suffix))
    backupFile = Path(targetDir).joinpath(fname)
    backupFile = Path(backupFile)
    shutil.copy(str(self), str(backupFile))



# Path.copy   = LnMonkey_copy
Path.LnCopy   = LnPathCopy
Path.LnBackup = LnPathBackup