#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################

# unicode tips https://www.safaribooksonline.com/library/view/fluent-python/9781491946237/ch04.html

# import os, sys

from LnLib.Common.LnLogger import SetLogger

def readTextFile(inputFname, encoding='utf-8', strip=True):
    logger = SetLogger(package=__name__)
    row = []
    logger.debug('reading file: {0}'.format(inputFname))
    try:
        f = open(inputFname, "r", encoding=encoding)
    except (Exception) as why:
        gv.Ln.Exit(1, str(why), printStack=True)

    for line in f:
        if strip:
            line = line.strip()
        row.append(line)
    f.close()

    logger.debug('number of lines read: {0}'.format(len(row)))
    return row

def readTextFile02(inputFname, encoding='utf-8'):
    row = []
    with open(inputFname, 'r', encoding=encoding) as f:
        row = f.read()
    row = row.split('\n').strip()

    return row


##############################################################
# - data deve essere una LIST
##############################################################
def WriteTextFile(outFname, data=[], encoding='utf-8'):
    logger = SetLogger(package=__name__)
    logger.debug('writing file:             {0}'.format(outFname))
    logger.debug('number of lines to write: {0}'.format(len(data)))

    nLines = 0
    newline = '\n'
    f = open(outFname, "w", encoding=encoding)
    for line in data:
        f.write('{0}{1}'.format(line, newline))
        nLines += 1

    f.close()

    return nLines



