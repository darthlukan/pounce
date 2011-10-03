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


# Now we are going to define the actual program API, these are the functions
# that are going to actually do work.  TODO: This still feels very "scripty" It
# needs to be cleaned up.

# The function that actually gets stuff
def getDownload(urlToGetFile, fileNameToSave):  # Grab the file(s)
    urllib.urlretrieve(urlToGetFile, fileNameToSave)

# This looks redundant now, but just wait... :)
def getSpecialDownload(urlToGetFile, baseDir):
    urllib.urlretrieve(urlToGetFile, baseDir)

def moreToDoQuery():
    moreDownloads = raw_input('Do you want to download more files?(y/n): ')
    if moreDownloads == 'n':
        print('Until next time!')
        exit(0)
    elif moreDownloads == 'y':
        print("""Do you need to loop over another file? Or do you only need to
        download from a single link?""")
        moreDownloadType = raw_input("""File Loop = 'loop', Single Link =
        'single': """)
        if moreDownloadType == 'loop':
            specialDownloadInfo()
        elif moreDownloadType == 'single':
            regDownloadInfo()
        else:
            print('Invalid response recorded, please try again.')
            moreToDoQuery()
    else:
        print("Let's try that again...")
        moreToDoQuery()    

def specialDownloadWork():
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
    urlToGetFile = raw_input("""Enter the filename (with path) that
    contains URLs: """)
    baseDir = raw_input("""Enter the directory path where you want the
    files saved: """)
    getSpecialDownload(urlToGetFile, baseDir)

def regDownloadInfo():
    urlToGetFile = raw_input('Please enter the download URL: ')
    fileNameToSave = raw_input('Enter the desired path and filename: ')
    getDownloadurlToGetFile, fileNameToSave()

# Loop over the file and grab some useful values for the progressbar output.
def getOverallLength(fileNameUrls):
    fi = fileinput.input(fileNameUrls)
    overallLength = 0
    for line in fi:
        data = str(urllib2.urlopen(line[:-1]).info())
        data = data[data.find('Content-Length'):]
        data = data[16:data.find('\r')]
        overallLength += int(data)
    return overallLength

def fileLoopCheck():
    specialDownload = raw_input('Do you need to import a file with links?(y/n): ')
    if specialDownload == 'n':
        regDownloadInfo()
    elif specialDownload == 'y':
        specialDownloadInfo()
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
