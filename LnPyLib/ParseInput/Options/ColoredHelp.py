#!/usr/bin/python3.5
#
# updated by ...: Loreto Notarantonio
# Version ......: 03-01-2018 10.14.03
#
# -----------------------------------------------


from  ... Common.LnColor import LnColor; C=LnColor()

################################################
# formatting help message
################################################
def coloredHelp(text, default=None, required=False):
    mandatory = C.getColored(color=C.yellowH, text='MANDATORY') if required else C.getColored(color=C.green, text='OPTIONAL')

    if not text:
        myHelp = ''
    else:
        myHelp   = '''{MANDATORY} - {TEXT}
        [DEFAULT: {DEFAULT}]
            '''.format(MANDATORY=mandatory, TEXT=C.getColored(color=C.yellow, text=text), DEFAULT=default)


    return myHelp