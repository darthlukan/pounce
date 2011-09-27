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
saveFileWhere = raw_input('Where do you want this file to be saved?: ')

# Define functions that will use our globals:
# Problem in this function:
#  File "/usr/lib/python2.7/urllib.py", line 91, in urlretrieve
#     return _urlopener.retrieve(url, filename, reporthook, data)
#   File "/usr/lib/python2.7/urllib.py", line 276, in retrieve
#     reporthook(blocknum, bs, size)
# TypeError: 'str' object is not callable
#
# TODO, use urllib properly
#
def getFile():  # Grab the file
    urllib.urlretrieve(urlToGet, fileName, saveFileWhere)

# Call our main function
getFile()


