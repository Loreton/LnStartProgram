#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

# updated by ...: Loreto Notarantonio
# Version ......: 19-08-2019 16.26.44

import sys, os

# ---- importing colorama as zip file...
# this_path = os.path.dirname(__file__)
# colorama = os.path.join(this_path, 'colorama.zip')
# sys.path.append(colorama)
# import colorama_039 as colorama
# or ...
from . import colorama_039 as colorama
# ----


class LnColor:
    colorama.init(wrap=True, convert=None, strip=None, autoreset=False)
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





    black       = FG.BLACK
    red         = FG.RED              ; redH     = red     + HI.BRIGHT
    green       = colorama.Fore.GREEN ; greenH   = green   + HI.BRIGHT
    yellow      = FG.YELLOW           ; yellowH  = yellow  + HI.BRIGHT
    blue        = FG.BLUE             ; blueH    = blue    + HI.BRIGHT
    magenta     = FG.MAGENTA          ; magentaH = magenta + HI.BRIGHT
    cyan        = FG.CYAN             ; cyanH    = cyan    + HI.BRIGHT
    white       = FG.WHITE            ; whiteH   = white   + HI.BRIGHT

    RESET        = HI.RESET_ALL
    BW           = FG.BLACK + BG.WHITE
    BWH          = FG.BLACK + BG.WHITE + HI.BRIGHT
    YelloOnBlack = FG.BLACK + BG.YELLOW

    normal = HI.RESET_ALL + FG.WHITE + BG.BLACK
    callerFunc = sys._getframe(1).f_code.co_name




        #  aliases
    error    = redH
    warning  = magentaH
    fucsia   = magentaH
    info     = greenH

    def __init__(self, filename=None):
        self._stdout = None
        self._stdout_colored = None

        if filename:
            name,ext = filename.rsplit('.',1)
            colored_filename = name + '_colored.' + ext

            self._stdout = open(filename, "w", encoding='utf-8')
            self._stdout_colored = open(colored_filename, "w", encoding='utf-8')


    def setColor(self,  color=''):
        print (self.normal + color, end='' )


    def getColored(self, **args):
        return self.printColored (fGET=True, **args)


    def printColored(self, color='', text='', tab=0, end='\n', autoreset=True, string_encode='latin-1', fGET=False):
        _function_name = sys._getframe().f_code.co_name
        thisTAB = ' '*tab
        if not isinstance(text, str):
            text = str(text)


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

        colored_text = '{0}{1}{2}'.format(thisTAB, color, text)
        normal_text = '{0}{1}'.format(thisTAB, text)

        # ----------------------------------------------
        # - print
        # ----------------------------------------------
        ret_val=None
        if fGET:
            ret_val=colored_text
        else:
            try:
                print (colored_text, end=end )

            except (UnicodeEncodeError):
                print ('{0} function: {1} - UnicodeEncodeError on next line'.format(
                        LnColor.redH,
                        _function_name),
                    end=end )
                print (normal_text.encode(string_encode, 'ignore'), end=end )

            finally:
                if self._stdout:
                    self._stdout.write('{0}{1}'.format(normal_text, end))
                if self._stdout_colored:
                    self._stdout_colored.write('{0}{1}'.format(colored_text, end))


        if autoreset:
            print(self.normal, end='')

        return ret_val
