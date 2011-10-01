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

# Explanation of import list:
# os and sys are needed to make sure that files and system level stuff
# are handled properly.  urllib(2) for communications (we are downloading)
# fileinput handles looping over links in a file (txt for now, csv later)
# progressbar adds some bling for the user to look at while we work.

import os
import sys
import urllib
import urllib2
import fileinput
from progressbar import ProgressBar

#Introduce ourselves
print("""Hello! I am going to ensure that downloading your file, renaming it,
and specifying where to save it, are as simple as possible. Let's get to it!""")

# Warn the user about non-existent feature
print('Be warned! File Looping has not yet been implemented and will cause an exit.')

# The function that actually gets stuff
# IT WORKS!!!
def getStandardDownload():  # Grab the file
    urllib.urlretrieve(urlToGetFile, fileNameToSave)

#Define initial globals,
specialDownload = raw_input('Do you need to import a file with links?(y/n): ')
if specialDownload == 'n':
    urlToGetFile = raw_input('Please enter the download URL: ')
    # raw_input is smarter than me, it allows for entering absolute paths to
    # desired filenames.  Go figure, the computer taught me something :)
    fileNameToSave = raw_input("""Enter the desired download location and filename
    (/home/username/downloads/filename.ext): """)
    getStandardDownload() # Main download function, no file loops...yet.
elif specialDownload == 'y':
    print('This feature has not yet been implemented! Please re-run the program')
    exit("Feature 'file looping' not yet implemented.")
else:
    print('There was a problem with your response, please re-run the program')
    exit("User input invalid or unreadable.")

# Call our main function
# getStandardDownload()


