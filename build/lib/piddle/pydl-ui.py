#!/usr/bin/env python2
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Filename: pydl-ui.py                                              #
# Authors: Brian Tomlinson <darthlukan@gmail.com>                   #
# URL: git@github.com:darthlukan/piddle.git                         #
# Description: A simple CLI download manager written in Python.     #
# Warning: If you received this program from any source other than  #
# the above noted URL, please check the source code! You may have   #
# downloaded a file with malicious code injected.                   #
# License: GPLv2, Please see the included LICENSE file.             #
# Note: This software should be considered experimental!            #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import os
import curses
import piddle.pydl as pydl
from threading import Thread as thread

class Caller():

    #def __init__(self):
        # TODO: Connect to the API and keep a thread open for communication.

    def get_param(self):
        self.screen.clear()
        self.screen.border(0)
        self.screen.refresh()
        query = self.screen.getstr(10, 10, 60)
        return query

    def execute_cmd(self):
        os.system("clear")
        a = thread(target=pydl.InfoGather.file_loop_check())
        print ""
        if a == 0:
             print "Command executed correctly"
        else:
             print "Command terminated with error"
        raw_input("Press enter")
        print ""

    def display(self):

        x = 0

        while x != ord('2'):
            screen = curses.initscr()

            screen.clear()
            screen.border(0)
            screen.addstr(2, 2, "Please enter a number...")
            screen.addstr(4, 4, "1 - I'm ready!")
            screen.addstr(5, 4, "2 - Exit plx")
            screen.refresh()

            x = screen.getch()

            if x == ord('1'):
                 self.execute_cmd()
                 curses.endwin()

        curses.endwin()