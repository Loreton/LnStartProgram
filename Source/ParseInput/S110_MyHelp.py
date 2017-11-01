#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
# updated by Loreto: 23-10-2017 17.51.47
# -----------------------------------------------

################################################
# formatting help message
################################################
def myHELP(text, default=None):
    if default:
        myHelp = '''{TEXT}
    [DEFAULT: {DEFAULT}]
        '''.format(TEXT=text, DEFAULT=default)
    else:
        myHelp = '''{TEXT}
        '''.format(TEXT=text)

    return myHelp


