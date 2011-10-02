#!/usr/bin/env python2
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Filename: pydl.py                                                 #
# Authors: Brian Tomlinson <darthlukan@gmail.com>                   #
#          Manuel Debaux <debaux.manual@gmail.com>                  #
#          Brian Turner <archkaine@gmail.com>                       #
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
# progressbar adds some bling for the user to look at while we work.  To get
# progressbar to work, pip2 install progressbar.

import os
import sys
import urllib
import urllib2
import fileinput
from progressbar import *

#Introduce ourselves
print("""Hello! I am going to ensure that downloading your file, renaming it,
and specifying where to save it, are as simple as possible. Let's get to it!""")

# Warn the user about non-existent feature
print('Be warned! File Looping has been implemented but is experimental.')
print('Downloading large groups of files could lead to RAM abuse.')
# The function that actually gets stuff
def getDownload(urlToGetFile, fileNameToSave):  # Grab the file(s)
    urllib.urlretrieve(urlToGetFile, fileNameToSave)

    # Placeholder for progressbar:
    #widgets = ['Overall Progress: ', Percentage(), ' ',
    #               Bar(marker='#',left='[',right=']'),
    #               ' ', ETA(), ' ', FileTransferSpeed()]
    #pbar = ProgressBar(widgets=widgets, maxval=nl)
    #pbar.start()

def fileLoopCheck():
    specialDownload = raw_input('Do you need to import a file with links?(y/n): ')
    if specialDownload == 'n':
        urlToGetFile = raw_input('Please enter the download URL: ')
        fileNameToSave = raw_input('Enter the desired filename: ')
        getDownload()
    elif specialDownload == 'y':
        fileNameUrls = raw_input('Enter the filename (with path) that contains URLs: ')
        baseDir = raw_input('Enter the directory where to download files: ')
        # Define how to handle pathing, default to preceding '/'
        if not baseDir.endswith("/"):
            baseDir+="/"
        # Grab the file and iterate over each line, this is not yet smart enough
        # to discern between an actual url and erroneous text, so don't have anything
        # other than links in your input file!
        fi = fileinput.input(fileNameUrls)
        nl=0 #numbers of line
        for line in fi:
            nl+=1 # iterate over the next line
        # Re-read, this will be cleaned up later
        fi = fileinput.input(fileNameUrls) # reset the fileinput : can't reuse it
        cl=0 # currentline
        # Progressbar() stuff, wheee!
        widgets = ['Overall Progress: ', Percentage(), ' ',
                       Bar(marker='>',left='[',right=']'),
                       ' ', ETA(), ' ', FileTransferSpeed()]
        pbar = ProgressBar(widgets=widgets, maxval=nl)
        pbar.start()
        # Done with the prep work, time to do what the user wants
        for line in fi:
            urlToGetFile=line[:-1]
            fileNameToSave=urlToGetFile[urlToGetFile.rfind('/')+1:]
            getDownload(urlToGetFile, fileNameToSave)
            cl+=1
            pbar.update(cl)
        pbar.finish()
        print('All done!')
    else:
        print('There was an error in your response, let\'s try again...')
        fileLoopCheck()
# Call start function
fileLoopCheck()
