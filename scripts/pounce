#!/usr/bin/env python
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Filename: pounce.py                                               #
# Authors: Brian Tomlinson <darthlukan@gmail.com>                   #
# URL: git@github.com:darthlukan/pounce.git                         #
# Description: A simple CLI downloader written in Python.           #
# Warning: If you received this program from any source other than  #
# the above noted URL, please check the source code! You may have   #
# downloaded a file with malicious code injected.                   #
# License: GPLv2, Please see the included LICENSE file.             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import os
import shutil
import argparse
import fileinput
import notify2
import multiprocessing
from progressbar import *
from urllib.request import urlopen


class Workers(object):
    """
    Provides methods that do all of the heavy lifting.  Methods contained
    require use of the InfoGather class methods prior to being called in
    order to function properly as a script.
    """

    def __init__(self):
        self.widgets = ['Download Progress: ', Percentage(), ' ',
                        Bar(marker='>', left='[', right=']'),
                        ' ', ETA(), ' ', FileTransferSpeed()]

    def more_to_do_query(self):
        """
        Called by other functions in order to provide an interface for users to
        continue to download files or to exit.
        """
        moreDownloads = self.query_response('Do you want to download more files?: ')
        if moreDownloads == 'n':
            print('Until next time!')
            return clean_exit()
        elif moreDownloads == 'y':
            print('Re-routing...')
            return InfoGather().file_loop_check()
        else:
            print('Something bad happened, please report this error to the creator.')
            return clean_exit()

    def query_response(self, question):
        """
        Holds command line responses and passes them to the appropriate
        functions.  If response is not 'q', returns response as string for
        processing.
        """
        prompt = " [y/n/q] "
        response = input(question + prompt).lower()
        if response == 'q':
            return clean_exit()
        elif response == 'y' or response == 'n':
            return response
        else:
            print('Invalid response recorded, please try again.\n')
            return self.query_response(question)

    def get_overall_length(self, fileNameUrls, baseDir):
        """
        Prepares the transaction for special downloads.  This is specific to urls
        contained in text files (for now, csv later).  Iterates over the provided
        file argument and sets each line to be downloaded in turn.
        """
        fi = fileinput.input(fileNameUrls)
        overallLength = 0
        for line in fi:
            data = urlopen(line)
            size = int(data.headers['Content-Length'].strip())
            overallLength += int(size)
        return self.special_download_work(fileNameUrls, baseDir, overallLength)

    def get_reg_download(self, urlToGetFile, fileNameToSave):
        """
        Pulls the remote file with urllib and displays a progressbar.
            Takes two arguments:

            urlToGetFile: string url (with filename) of the file we want to
            download.

            fileNameToSave: string absolute path and filename that we want to end
            up with.  If no path is given, the cwd is the target.  Breaks if no
            write permissions to cwd!

            returns/redirects to more_to_do_query() on completion.
        """
        filelen = 0
        data = urlopen(urlToGetFile, timeout=60)
        size = int(data.headers["Content-Length"].strip())
        filelen += int(size)

        # Sets up progressbar:
        widgets = self.widgets
        pbar = ProgressBar(widgets=widgets, maxval=filelen).start()

        fileNameToSave = os.path.join(fileNameToSave, urlToGetFile[urlToGetFile.rfind('/') + 1:])
        # This actually grabs the file. Thanks to BlaXpirit via http://goo.gl/V910H
        with urlopen(urlToGetFile, timeout=60) as response, open(fileNameToSave, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)

        # Place in own class and thread?
        for i in range(filelen):
            pbar.update(i + 1)
        pbar.finish()
        note_set_and_send('Pounce: ', '%s download complete!' % fileNameToSave)
        return self.more_to_do_query()

    def special_download_work(self, fileNameUrls, baseDir, overallLength):
        """
        The actual worker for special downloads.  Must be called by
        get_overall_length() in order to work! Calls get_special_download() on
        each line of the file provided in order to download the desired files.
        """
        if not baseDir.endswith('/') and baseDir != '':
            baseDir += '/'
        fi = fileinput.input(fileNameUrls)
        nl = 0
        for line in fi:
            nl += 1
        fi = fileinput.input(fileNameUrls)
        cl = 0
        widgets = self.widgets
        pbar = ProgressBar(widgets=widgets, maxval=overallLength)
        pbar.start()
        for line in fi:
            urlToGetFile = line[:-1]
            fileNameToSave = os.path.join(baseDir, urlToGetFile[urlToGetFile.rfind('/') + 1:])
            self.get_special_download(urlToGetFile, fileNameToSave)
            cl += 1
            pbar.update(overallLength / nl * cl)
            for i in range(overallLength):
                pbar.update(i + 1)
            note_set_and_send('Pounce: ', '%s download complete!' % fileNameToSave)
        pbar.finish()
        print('All done!')
        return self.more_to_do_query()

    def get_special_download(self, urlToGetFile, baseDir):
        """
        Takes the individual links from the file input in special_download_work(),
        downloads the object that the URL points to, and copies it to the output directory/file.

        returns the status of shutil.copyfileobj()
        """
        with urlopen(urlToGetFile, timeout=60) as response, open(baseDir, 'wb') as out_file:
            return shutil.copyfileobj(response, out_file)


class InfoGather(object):
    """
    Contains methods related to information gathering. Provides basic text
    interface for terminal users.
    """

    def __init__(self):
        self.work = Workers()

    def special_download_info(self):
        """
        Gathers information based on special download requests.  Accepts a
        file as input and passes it to the relevant function.  Provides ability
        for users to exit cleanly based on input.
        """
        fileNameUrls = input('Enter the filename (with path) that contains URLs (Q to quit): ')
        if fileNameUrls.upper() == 'Q':
            return clean_exit()
        baseDir = input('Enter the directory path where you want the files saved (Q to quit): ')
        if baseDir.upper() == 'Q':
            return clean_exit()
        return self.work.get_overall_length(fileNameUrls, baseDir)

    def reg_download_info(self):
        """
        Gathers information based on regular download requests. Takes a url
        and passes it to the relevant function.  Provides ability for users
        to exit cleanly based on input.
        """
        urlToGetFile = input('Please enter the download URL (Q to quit): ')
        if urlToGetFile.upper() == 'Q':
            return clean_exit()
        fileNameToSave = input('Enter the desired path and filename (Q to quit): ')
        if fileNameToSave.upper() == 'Q':
            return clean_exit()
        return self.work.get_reg_download(urlToGetFile, fileNameToSave)

    def file_loop_check(self):
        """Queries the user and directs them based on input."""
        specialDownload = self.work.query_response('Do you need to import a file with links?')
        if specialDownload == 'n':
            return self.reg_download_info()
        elif specialDownload == 'q':
            return clean_exit()
        else:
            return self.special_download_info()


def note_set_and_send(app, summary):
    """
    Creates a DBUS notification.
    """
    notify2.init('Pounce: ')
    return notify2.Notification(app, summary).show()


def clean_exit():
    """
    If we call this, we are exiting based on user input and not because of an
    error.
    """

    print("Thank you for using Pounce.")
    exit(0)


def main():
    """
    Parses arguments and calls relevant functions and methods.
    """
    VERSION = '1.0'

    parser = argparse.ArgumentParser(description='pounce argument information.')
    parser.add_argument('-f', '--file', nargs='*',  action='append', dest='cFiles',
                        help='Given the full path,load each URL in the file.')
    parser.add_argument('-u', '--url', nargs='*', action='append', dest='cUrls',
                        help='This will grab 1 url.')
    parser.add_argument('-o', '--output', nargs=1,  action='store', dest='outputDir',
                        help='Move all downloaded files to this directory.')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s-' + VERSION,
                        help='Current version of pounce.py')

    ig = InfoGather()

    args = parser.parse_args()
    if args.cFiles:
        for file in args.cFiles:
            p = multiprocessing.Process(
                target=Workers().get_overall_length(fileNameUrls=file, baseDir=args.outputDir[0]))
            p.start()
    elif args.cUrls:
        for url in args.cUrls:
            p = multiprocessing.Process(
                target=Workers().get_reg_download(urlToGetFile=url[0], fileNameToSave=args.outputDir[0]))
            p.start()
    else:
        ig.file_loop_check()

if __name__ == '__main__':
    main()