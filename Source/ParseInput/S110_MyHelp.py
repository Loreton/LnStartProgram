#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
# updated by Loreto: 23-10-2017 17.51.47
# -----------------------------------------------


from LnLib.Common.LnColor import LnColor
C=LnColor()

################################################
# formatting help message
################################################
def myHELP(text, default=None, required=False):
    mandatory = C.getColored(color=C.yellowH, text='MANDATORY') if required else C.getColored(color=C.green, text='OPTIONAL')

    if not text:
        myHelp = ''
    else:
        myHelp   = '''{MANDATORY} - {TEXT}
        [DEFAULT: {DEFAULT}]
            '''.format(MANDATORY=mandatory, TEXT=C.getColored(color=C.yellow, text=text), DEFAULT=default)


    return myHelp