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

import os
import urllib2
import argparse
import fileinput
import notify2
from progressbar import *
from threading import Thread


class Workers:
    '''
    Provides methods that do all of the heavy lifting.  Methods contained
    require use of the InfoGather class methods prior to being called in
    order to function properly as a script.
    '''

    def query_response(self, question):
        '''
        Holds command line responses and passes them to the appropriate
        functions.  If response is not "q", returns response as string for
        processing.
        '''
        prompt = " [y/n/q] "
        response = raw_input(question + prompt).lower()
        if response == 'q':
            clean_exit()
        elif response == 'y' or response == 'n':
            return response;
        else:
            print('Invalid response recorded, please try again.\n')
            self.query_response(question)

    def get_reg_download(self, urlToGetFile, fileNameToSave):
        '''
        Pulls the remote file with urllib2 and displays a progressbar.
            Takes two arguments:

            urlToGetFile: string url (with filename) of the file we want to
            download.

            fileNameToSave: string absolute path and filename that we want to end
            up with.  If no path is given, the cwd is the target.  Breaks if no
            write permissions to cwd!

            returns nothing, redirects to more_to_do_query() on completion.
        '''
        filelen=0
        data=str(urllib2.urlopen(urlToGetFile).info())
        data=data[data.find("Content-Length"):]
        data=data[16:data.find("\r")]
        filelen+=int(data)

        # Sets up progressbar:
        widgets = ['Download Progress: ', Percentage(), ' ',
                       Bar(marker='>', left='[',right=']'),
                       ' ', ETA(), ' ', FileTransferSpeed()]
        pbar = ProgressBar(widgets=widgets, maxval=filelen).start()

        # This actually grabs the file.
        urllib2.urlopen(urlToGetFile, fileNameToSave)

        # Place in own class and thread?
        for i in range(filelen):
            pbar.update(i+1)
        pbar.finish()
        note_set_and_send('Piddle: ', '%s download complete!' % fileNameToSave)
        self.more_to_do_query()

    # This looks redundant now, but just wait... :)
    def get_special_download(self, urlToGetFile, baseDir):
        urllib2.urlopen(urlToGetFile, baseDir)

    def get_overall_length(self, fileNameUrls, baseDir):
        '''
        Prepares the transaction for special downloads.  This is specific to urls
        contained in text files (for now, csv later).  Iterates over the provided
        file argument and sets each line to be downloaded in turn.
        '''
        fi = fileinput.input(fileNameUrls)
        overallLength = 0
        for line in fi:
            data = str(urllib2.urlopen(line).info())
            data = data[data.find('Content-Length'):]
            data = data[16:data.find('\r')]
            overallLength += int(data)
        self.special_download_work(fileNameUrls, baseDir, overallLength)

    def more_to_do_query(self):
        '''
        Called by other functions in order to provide an interface for users to
        continue to download files or to exit.
        '''
        moreDownloads = self.query_response('Do you want to download more files?(y/n): ')
        if moreDownloads == 'n':
            print('Until next time!')
            clean_exit()
        elif moreDownloads == 'y':
                print('Re-routing...')
                ig.file_loop_check()
        else:
            print('Something bad happened, please report this error to the creator.')
            clean_exit()

    def special_download_work(self, fileNameUrls, baseDir, overallLength):
        '''
        The actual worker for special downloads.  Must be called by
        get_overall_length() in order to work! Calls get_special_download() on
        each line of the file provided in order to download the desired files.
        '''
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
            fileNameToSave = os.path.join(baseDir,urlToGetFile[urlToGetFile.rfind('/')+1:])
            self.get_special_download(urlToGetFile, fileNameToSave)
            cl += 1
            pbar.update(overallLength / nl * cl)
            for i in xrange(overallLength):
                pbar.update(i+1)
        pbar.finish()
        print('All done!')
        note_set_and_send('Piddle: ', '%s download complete!' % (fileNameToSave))
        self.more_to_do_query()


class InfoGather:
    '''
    Contains methods related to information gathering. Provides basic text
    interface for terminal users.
    '''

    def __init__(self):
        self.work = Workers()

    def special_download_info(self):
        '''
        Gathers information based on special download requests.  Accepts a
        file as input and passes it to the relevant function.  Provides ability
        for users to exit cleanly based on input.
        '''
        fileNameUrls = raw_input('Enter the filename (with path) that contains URLs (Q to quit): ')
        if fileNameUrls.upper() == 'Q':
            clean_exit()
        baseDir = raw_input('Enter the directory path where you want the files saved (Q to quit): ')
        if baseDir.upper() == 'Q':
            clean_exit()
        self.work.get_overall_length(fileNameUrls, baseDir)

    def reg_download_info(self):
        '''
        Gathers information based on regular download requests. Takes a url
        and passes it to the relevant function.  Provides ability for users
        to exit cleanly based on input.
        '''
        urlToGetFile = raw_input('Please enter the download URL (Q to quit): ')
        if urlToGetFile.upper() == 'Q':
            clean_exit()
        fileNameToSave = raw_input('Enter the desired path and filename (Q to quit): ')
        if fileNameToSave.upper() == 'Q':
            clean_exit()
        self.work.get_reg_download(urlToGetFile, fileNameToSave)

    def file_loop_check(self):
        '''Queries the user and directs them based on input.'''
        specialDownload = self.work.query_response('Do you need to import a file with links?')
        if specialDownload == 'n':
            self.reg_download_info()
        else:
            self.special_download_info()


def note_set_and_send(app, summary):
    '''
    Creates a DBUS notification.
    '''
    notify2.init('Piddle: ')
    return notify2.Notification(app, summary).show()


def clean_exit():
    '''
    If we call this, we are exiting based on user input and not because of an
    error.
    '''

    print ("Thank you for using piddle.")
    exit(0)


def main():
    '''
    Greets the user, requests and parses arguments, and calls relevant
    functions and methods.
    '''
    VERSION = '0.2.dev'

    print("Hello! I am going to ensure that downloading your files, renaming them, ")
    print("and specifying where to save them, are as simple as possible. Let's get to it!")

    parser = argparse.ArgumentParser(description='pydl argument information.')
    parser.add_argument('-f', '--file', nargs='*',  action='append', dest='cFiles',
           help='Given the full path load each URL in the file. This will also take multiple file arguments.')
    parser.add_argument('-d', '--dir',   nargs=1, action= 'store', default=".", dest='outputDir',
           help='In a given directory check all files for URLs and download those.')
    parser.add_argument('-u', '--url', nargs='*', action='append', dest='cUrls',
           help='This will grab 1-N urls. Use space as the delimitter.')
    parser.add_argument('-o', '--output', nargs=1,  action='store', dest='outputDir',
           help='Move all downloaded files to this directory.')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s-' + VERSION,
           help ='Current version of pydl.py')

    ig = InfoGather()

    args = parser.parse_args()
    if(args.cFiles):
        for file in args.cFiles:
            tx = Thread(target=getOverallLength(file,args.outputDir[0]))
            print("thread start")
            tx.start()
    elif(args.cUrls):
            for url in args.cUrls:
                print("this hasn't been configured yet.")
    else:
        ig.file_loop_check()

if __name__ == '__main__':
    main()