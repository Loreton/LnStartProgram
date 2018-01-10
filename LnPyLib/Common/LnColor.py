#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import sys
from . import colorama

class LnColor:
    colorama.init(autoreset=True)
    # for i in dir('LnColors'): print (i)
    '''
        devo mantenere i valori seguenti perché a volte
        devo mandare una stringa pronta con il colore e non posso usare il printColor(msg) oppure il getColor()
        in quanto ho una stringa multicolor
        usageMsg = " {COLOR}   {TEXT} {COLRESET}[options]".format(COLOR=C.YEL, TEXE='Loreto', COLRESET=C.RESET)

    '''
    FG         = colorama.Fore
    BG         = colorama.Back
    HI         = colorama.Style


    critical   = FG.BLUE
    info       = FG.GREEN
    black      = FG.BLACK
    red        = FG.RED
    green      = colorama.Fore.GREEN
    yellow     = FG.YELLOW
    blue       = FG.BLUE
    magenta    = FG.MAGENTA
    # FUCSIA     = FG.MAGENTA + HI.BRIGHT
    cyan       = FG.CYAN
    white      = FG.WHITE

    redH       = FG.RED     + HI.BRIGHT
    greenH     = FG.GREEN   + HI.BRIGHT
    yellowH    = FG.YELLOW  + HI.BRIGHT
    cyanH      = FG.CYAN    + HI.BRIGHT
    magentaH   = FG.MAGENTA + HI.BRIGHT
    # FUCSIAH    = FG.FUCSIA  + HI.BRIGHT

    RESET      = HI.RESET_ALL

    BW         = FG.BLACK + BG.WHITE
    BWH        = FG.BLACK + BG.WHITE + HI.BRIGHT
    YelloOnBlack        = FG.BLACK + BG.YELLOW


    callerFunc = sys._getframe(1).f_code.co_name




        #  aliases
    error  = redH
    warning  = magentaH
    fucsia  = magentaH






    def getColored(self, **args):
        return self.printColored (fGET=True, **args)

    def printColored(self, color=None, text=None, tab=0, end='\n', reset=True, string_encode='latin-1', fGET=False):
        endColor = self.RESET if reset else ''
        thisTAB = ' '*tab

        # if text == None:
        #     text = 'None'
        # elif text == False:
        #     text = 'False'
        # elif text == True:
        #     text = 'True'
        # ----------------------------------------------
        # - intercettazione del tipo text per fare un
        # - print più intelligente.
        # ----------------------------------------------
            # - convertiamo bytes in string
        if isinstance(text, bytes):
            text = text.decode('utf-8')

            # - convertiamo list in string (con il tab in ogni riga)
        if isinstance(text, list):
            myMsg = []
            for line in text:
                myMsg.append('{}{}'.format(thisTAB, line))
            text = '\n'.join(myMsg)
            thisTAB = ''

            # - aggiungiamo il tab in ogni riga
        elif '\n' in text:
            myMsg = []
            for line in text.split('\n'):
                myMsg.append('{}{}'.format(thisTAB, line))
            text = '\n'.join(myMsg)
            thisTAB = ''

        # PAD=' '*5
        # outText = '{0}{1}{2}{3}{4}'.format(thisTAB, color, text, endColor, PAD)
        outText = '{0}{1}{2}{3}'.format(thisTAB, color, text, endColor)

        # ----------------------------------------------
        # - print
        # ----------------------------------------------

        # callerFunc = sys._getframe(1).f_code.co_name
        # if callerFunc.startswith('get'):
        #     return outText
        if fGET:
            return outText
        else:
            try:
                print (outText, end=end )

            except (UnicodeEncodeError):
                print (color, text.encode(string_encode), endColor, end=end )

            finally:
                return None



