#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
# updated by Loreto: 23-10-2017 17.51.47
# -----------------------------------------------


from LnLib.Common.LnColor import LnColor
C=LnColor()
# printColored=C.printColored
# getColored=C.getColored
################################################
# formatting help message
################################################
# def myHELP_(text, default=None, required=False):
#     mandatory = C.getYellowH('MANDATORY - ') if required else 'OPTIONAL - '
#     if default:
#         myHelp = '''{TEXT}
#     [DEFAULT: {DEFAULT}]
#         '''.format(TEXT=text, DEFAULT=default)
#     else:
#         myHelp = '''{TEXT}
#         '''.format(TEXT=text)

#     return myHelp


################################################
# formatting help message
################################################
def myHELP(text, default=None, required=False):
    # mandatory = 'MANDATORY' if required else 'OPTIONAL'
    mandatory = C.getColored(color=C.yellowH, text='MANDATORY') if required else C.getColored(color=C.green, text='OPTIONAL')

    if not text:
        myHelp = ''
    else:
        myHelp   = '''{MANDATORY} - {TEXT}
        [DEFAULT: {DEFAULT}]
            '''.format(MANDATORY=mandatory, TEXT=C.getColored(color=C.yellow, text=text), DEFAULT=default)


    return myHelp