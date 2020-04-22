#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

# updated by ...: Loreto Notarantonio
# Version ......: 19-08-2019 12.46.46
import sys

# def keyb_input(msg, validKeys='ENTER', exitKeys='x'):
def keyb_input(msg, validKeys, exitKeys='x'):
    msg = "{msg} [{validKeys}] - ({exitKeys} to exit) ==> ".format(**locals())
    validKeys = validKeys.split('|')
    exitKeys = exitKeys.split('|')
    while True:
        choice      = input(msg).strip()
        choiceUPP   = choice.upper()
        if choice == '':    # diamo priorità alla exit
            if "ENTER" in exitKeys:
                sys.exit()
            elif "ENTER" in validKeys:
                return ''
            else:
                print('\n... please enter something\n')

        elif choice in exitKeys:
            print("Exiting on user request new.")
            sys.exit(1)

        elif choice in validKeys:
            break

        else:
            print('\n... try again\n')

    return choice

