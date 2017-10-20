#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import sys
import colorama

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

    CRITICAL   = FG.BLUE
    # ERROR      = FG.RED
    WARNING    = FG.MAGENTA
    INFO       = FG.GREEN

    BLACK      = FG.BLACK
    RED        = FG.RED
    GREEN      = colorama.Fore.GREEN
    YELLOW     = FG.YELLOW
    BLUE       = FG.BLUE
    MAGENTA    = FG.MAGENTA
    # FUCSIA     = FG.MAGENTA + HI.BRIGHT
    CYAN       = FG.CYAN
    WHITE      = FG.WHITE

    REDH       = FG.RED     + HI.BRIGHT
    GREENH     = FG.GREEN   + HI.BRIGHT
    YELLOWH    = FG.YELLOW  + HI.BRIGHT
    CYANH      = FG.CYAN    + HI.BRIGHT
    MAGENTAH   = FG.MAGENTA + HI.BRIGHT
    # FUCSIAH    = FG.FUCSIA  + HI.BRIGHT

    RESET      = HI.RESET_ALL

    BW         = FG.BLACK + BG.WHITE
    BWH        = FG.BLACK + BG.WHITE + HI.BRIGHT
    YelloOnBlack        = FG.BLACK + BG.YELLOW


    callerFunc = sys._getframe(1).f_code.co_name


    def YellowRev(self, msg, tab=0, end='\n', reset=True, string_encode='latin-1'):
        self._print (tab, self.YelloOnBlack, msg, end, reset)

    def Yellow(self, msg, tab=0, end='\n', reset=True, string_encode='latin-1'):
        self._print ( tab, self.YELLOW, msg, end, reset)

    def YellowH(self, msg, tab=0, end='\n', reset=True, string_encode='latin-1'):
        self._print ( tab, self.YELLOWH, msg, end, reset)



    def Green(self, msg, tab=0, end='\n', reset=True, string_encode='latin-1'):
        self._print ( tab, self.GREEN, msg, end, reset)

    def GreenH(self, msg, tab=0, end='\n', reset=True, string_encode='latin-1'):
        self._print ( tab, self.GREENH, msg, end, reset)



    def Blue(self, msg, tab=0, end='\n', reset=True, string_encode='latin-1'):
        self._print ( tab, self.BLUE, msg, end, reset)



    def Magenta(self, msg, tab=0, end='\n', reset=True, string_encode='latin-1'):
        self._print ( tab, self.MAGENTA, msg, end, reset)

    def MagentaH(self, msg, tab=0, end='\n', reset=True, string_encode='latin-1'):
        self._print ( tab, self.MAGENTAH, msg, end, reset)

    def Cyan(self, msg, tab=0, end='\n', reset=True, string_encode='latin-1'):
        self._print ( tab, self.CYAN, msg, end, reset)

    def CyanH(self, msg, tab=0, end='\n', reset=True, string_encode='latin-1'):
        self._print ( tab, self.CYANH, msg, end, reset)

    def White(self, msg, tab=0, end='\n', reset=True, string_encode='latin-1'):
        self._print ( tab, self.WHITE, msg, end, reset)

    def Red(self, msg, tab=0, end='\n', reset=True, string_encode='latin-1'):
        self._print ( tab, self.RED, msg, end, reset)

    def RedH(self, msg, tab=0, end='\n', reset=True, string_encode='latin-1'):
        self._print ( tab, self.REDH, msg, end, reset)


        # -----------------------------------------------
        # - ritorna una stringa colorata come richiesto
        # -----------------------------------------------
    def getYellow(self, msg, tab=0, end='\n', reset=True, string_encode='latin-1'):
        return self._print ( tab, self.YELLOW, msg, end, reset)

    def getYellowH(self, msg, tab=0, end='\n', reset=True, string_encode='latin-1'):
        return self._print ( tab, self.YELLOWH, msg, end, reset)

    def getGreen(self, msg, tab=0, end='\n', reset=True, string_encode='latin-1'):
        return self._print ( tab, self.GREEN, msg, end, reset)

    def getBlue(self, msg, tab=0, end='\n', reset=True, string_encode='latin-1'):
        return self._print ( tab, self.BLUE, msg, end, reset)

    def getMagenta(self, msg, tab=0, end='\n', reset=True, string_encode='latin-1'):
        return self._print ( tab, self.MAGENTA, msg, end, reset)

    def getMagentaH(self, msg, tab=0, end='\n', reset=True, string_encode='latin-1'):
        return self._print ( tab, self.MAGENTAH, msg, end, reset)

    def getCyan(self, msg, tab=0, end='\n', reset=True, string_encode='latin-1'):
        return self._print ( tab, self.CYAN, msg, end, reset)

    def getCyanH(self, msg, tab=0, end='\n', reset=True, string_encode='latin-1'):
        return self._print ( tab, self.CYANH, msg, end, reset)

    def getWhite(self, msg, tab=0, end='\n', reset=True, string_encode='latin-1'):
        return self._print ( tab, self.WHITE, msg, end, reset)

    def getRed(self, msg, tab=0, end='\n', reset=True, string_encode='latin-1'):
        return self._print ( tab, self.RED, msg, end, reset)

    def getRedH(self, msg, tab=0, end='\n', reset=True, string_encode='latin-1'):
        return self._print ( tab, self.REDH, msg, end, reset)




        #  aliases
    YEL         = YELLOW

    Error  = RedH
    # getREDH     = printRedH
    # getYellow   = printYellow
    # getGreen    = printGreen
    # getFucsia   = printFucsia
    # getWhite    = printWhite
    # getMagenta  = printMagenta
    # getCyan     = printCyan


        # common

    def _print_2(self, color, msg, end, reset=True, string_encode='latin-1'):
        endColor = self.RESET if reset else ''

        outText = '{0}{1}{2}'.format(color, msg, endColor)

        callerFunc = sys._getframe(1).f_code.co_name
        # print ('....2', callerFunc)
        if callerFunc.startswith('get'):
            return outText

        else:
            try:
                print (outText, end=end )

            except (UnicodeEncodeError):
                print (color, msg.encode(string_encode), endColor, end=end )

            finally:
                return None



    def _print(self, tab, color, text, end, reset=True, string_encode='latin-1'):
        endColor = self.RESET if reset else ''
        # print (text)
        # print (type(text))
        thisTAB = ' '*tab

        # ----------------------------------------------
        # - intercettazione del tipo text per fare un
        # - print più intelligente.
        # ----------------------------------------------
            # - convertiamo bytes in string
        if isinstance(text, bytes):
            text = text.decode('utf-8')
            # print (type(text))

            # - convertiamo list in string (con il tab in ogni riga)
        if isinstance(text, list):
            myMsg = []
            for line in text:
                myMsg.append('{}{}'.format(thisTAB, line))
            text = '\n'.join(myMsg)
            thisTAB = ''
            # outText = '{0}{1}{2}'.format(color, text, endColor)

            # - aggiungiamo il tab in ogni riga
        elif '\n' in text:
            myMsg = []
            for line in text.split('\n'):
                myMsg.append('{}{}'.format(thisTAB, line))
            text = '\n'.join(myMsg)
            thisTAB = ''
            # outText = '{0}{1}{2}'.format(color, text, endColor)

        # else:
        outText = '{0}{1}{2}{3}'.format(thisTAB, color, text, endColor)

        # ----------------------------------------------
        # - print
        # ----------------------------------------------

        callerFunc = sys._getframe(1).f_code.co_name
        if callerFunc.startswith('get'):
            return outText
        else:
            try:
                print (outText, end=end )

            except (UnicodeEncodeError):
                print (color, text.encode(string_encode), endColor, end=end )

            finally:
                return None


