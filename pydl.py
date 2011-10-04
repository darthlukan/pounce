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
from decimal import *

# Now we are going to define the actual program API, these are the functions
# that are going to actually do work.  TODO: This still feels very "scripty" It
# needs to be cleaned up.


# A function to provide a clean exit from anywhere in the program
def cleanExit():
    print ("Exiting now!")
    exit(0)

# The function that actually gets stuff
def getRegDownload(urlToGetFile, fileNameToSave):  # Grab the file(s)
    urllib.urlretrieve(urlToGetFile, fileNameToSave)

# This looks redundant now, but just wait... :)
def getSpecialDownload(urlToGetFile, baseDir):
    urllib.urlretrieve(urlToGetFile, baseDir)

def getOverallLength(fileNameUrls, baseDir):
    fi = fileinput.input(fileNameUrls)
    overallLength = 0
    for line in fi:
        data = str(urllib2.urlopen(line).info())
        data = data[data.find('Content-Length'):]
        data = data[16:data.find('\r')]
        overallLength += int(data)
    specialDownloadWork(fileNameUrls, baseDir, overallLength)

def moreToDoQuery():
    moreDownloads = raw_input('Do you want to download more files?(y/n/q): ')
    if moreDownloads == 'n'\
    or moreDownloads == 'N'\
    or moreDownloads == 'q'\
    or moreDownloads == 'Q':
        print('Until next time!')
        cleanExit()
    elif moreDownloads == 'y' or moreDownloads == 'Y':
        print("""Do you need to loop over another file? Or do you only need to
        download from a single link?""")
        moreDownloadType = raw_input("File Loop = 'loop', Single Link = 'single', or 'Q' to Quit: ")
        if moreDownloadType == 'loop' or moreDownloadType == 'l':
            specialDownloadInfo()
        elif moreDownloadType == 'single' or moreDownloadType == 's':
            regDownloadInfo()
        elif moreDownloadType == 'Q' or moreDownloadType == 'q':
            cleanExit()
        else:
            print('Invalid response recorded, please try again.')
            moreToDoQuery()
    else:
        print("Let's try that again...")
        moreToDoQuery()

def specialDownloadWork(fileNameUrls, baseDir, overallLength):
    if not baseDir.endswith('/') and baseDir != '':
        baseDir += '/'
    fi = fileinput.input(fileNameUrls)
    nl = 0
    for line in fi:
        nl += 1
    fi = fileinput.input(fileNameUrls)
    cl = 0
    widgets = ['Overall Progress: ', Percentage(), ' ',
                Bar(marker = '>', left = '[', right = ']'),
                ' ', ETA(), ' ', FileTransferSpeed()]
    pbar = ProgressBar(widgets = widgets, maxval = overallLength)
    pbar.start()
    for line in fi:
        urlToGetFile = line[:-1]
        fileNameToSave = baseDir + urlToGetFile[urlToGetFile.rfind('/')+1:]
        getSpecialDownload(urlToGetFile, fileNameToSave)
        cl += 1
        pbar.update(overallLength / nl * cl)
    pbar.finish()
    print('All done!')
    moreToDoQuery()

#This function is going to handle our special download info for file looping.
def specialDownloadInfo():
    fileNameUrls = raw_input('Enter the filename (with path) that contains URLs (Q to quit): ')
    if fileNameUrls == 'q' or fileNameUrls == 'Q':
        cleanExit()
    baseDir = raw_input('Enter the directory path where you want the files saved (Q to quit): ')
    if baseDir == 'q' or baseDir == 'Q':
        cleanExit()
    getOverallLength(fileNameUrls, baseDir)

def regDownloadInfo():
    urlToGetFile = raw_input('Please enter the download URL (Q to quit): ')
    if urlToGetFile == 'q' or urlToGetFile == 'Q':
        cleanExit()
    fileNameToSave = raw_input('Enter the desired path and filename (Q to quit): ')
    if fileNameToSave == 'q' or fileNameToSave == 'Q':
        cleanExit()
    getRegDownload(urlToGetFile, fileNameToSave)

def fileLoopCheck():
    specialDownload = raw_input('Do you need to import a file with links?(y/n/q): ')
    if specialDownload == 'n' or specialDownload == 'N':
        regDownloadInfo()
    elif specialDownload == 'y' or specialDownload == 'Y':
        specialDownloadInfo()
    elif specialDownload == 'q' or specialDownload == 'Q':
        cleanExit()
    else:
        print("There was an error in your response, let's try again...")
        fileLoopCheck()

def main():
    print("""Hello! I am going to ensure that downloading your files, renaming them,
             and specifying where to save them, are as simple as possible. Let's get to it!""")
    print('Be warned! File Looping has been implemented but is experimental.')
    print('Downloading large groups of files could lead to RAM abuse.')
    fileLoopCheck()

# Call main function
main()