#!/usr/bin/python3.4
# -*- coding: iso-8859-15 -*-
#
#!/usr/bin/python -O
# -O Optimize e non scrive il __debug__
#
# ####################################################################################################################
import subprocess

from .. Logger.SetLogger import SetLogger
# from LnLib.Common.LnColor  import LnColor
# from LnLib.Common.Exit     import Exit

##########################################################
# - timeout     solo dalla Versione 3.3
# - extraParam  conterrà magari parametri con blank in mezzo
##########################################################
def ExecRcode(command, timeout=None, EXECUTE=True, shell=False):
    logger = SetLogger(package=__name__)


    if isinstance(command, list):
        cmdLIST = command

    elif isinstance(command, str):
        cmdLIST = [x.strip() for x in command.split()]

    if shell:
        cmdLIST = ' '.join(cmdLIST)                      # Join command

    logger.debug('[dry-run: {DRYRUN}] - executing command "{0}"'.format(command, DRYRUN=not EXECUTE))

    if EXECUTE:
        logger.info(' EXEC:    {0}'.format(' '.join(cmdLIST)))
        import os
        # devnull = open(os.devnull, 'w')
        try:
            with open(os.devnull, "wb") as devnull:
                rCode = subprocess.call( cmdLIST, shell=shell, stdout=devnull, stderr=devnull, timeout=timeout)  # ritorna <class 'bytes'>

        except subprocess.TimeoutExpired as why:
            msg = str(why)
            logger.error(msg)
            # rCode = 9

    else:
        logger.info(' DRY-RUN: {0}'.format(command))
        rCode = 0

    if rCode:
        logger.error('rcode: {0}'.format(rCode))

    return rCode

    '''  ALTRO metodo

    '''
