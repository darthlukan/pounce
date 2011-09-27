#!/usr/bin/env python2
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Filename: pydl.py                                                 #
# Author: Brian Tomlinson <darthlukan@gmail.com>                     #
# URL: git@github.com:darthlukan/piddle.git                         #
# Description: A simple CLI download manager written in Python.     #
# Warning: If you received this program from any source other than  #
# the above noted URL, please check the source code! You may have   #
# downloaded a file with malicious code injected.                   #
# License: GPLv2, Please see the included LICENSE file.             #
# Note: This software should be considered experimental!            #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import os
import sys
import urllib
import urllib2
from progressbar import ProgressBar

#Introduce ourselves
print("""Hello! I am going to ensure that downloading your file, renaming it,
and specifying where to save it, are as simple as possible. Let's get to it!""")

#Define our globals
urlToGet = raw_input('Please enter the download URL: ')
fileName = raw_input('Enter the desired filename: ')

# The function that actually gets stuff
# IT WORKS!!!
def getFile():  # Grab the file
    urllib.urlretrieve(urlToGet, fileName)

# Call our main function
getFile()


