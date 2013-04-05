#!/usr/bin/env python
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Filename: pydl.py                                                 #
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
import csv
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
        widgets = ['Download Progress: ', Percentage(), ' ',
                   Bar(marker='>', left='[', right=']'),
                   ' ', ETA(), ' ', FileTransferSpeed()]
        pbar = ProgressBar(widgets=widgets, maxval=filelen).start()

        # This actually grabs the file. Thanks to BlaXpirit via http://goo.gl/V910H
        with urlopen(urlToGetFile, timeout=60) as response, open(fileNameToSave, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)

        # Place in own class and thread?
        for i in range(filelen):
            pbar.update(i + 1)
        pbar.finish()
        note_set_and_send('Piddle: ', '%s download complete!' % fileNameToSave)
        return self.more_to_do_query()

    # This looks redundant now, but just wait... :)
    def get_special_download(self, urlToGetFile, baseDir):
        with urlopen(urlToGetFile, timeout=60) as response, open(baseDir, 'wb') as out_file:
            return shutil.copyfileobj(response, out_file)

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

    def get_csv_overall_length(self, csvFile, baseDir):
        overallLength = 0
        with open(csvFile, newline='') as csvfile:
            spreadsheet = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spreadsheet:
                data = urlopen(row[0])
                size = int(data.headers['Content-Length'].strip())
                overallLength += int(size)
        return self.csv_download_work(csvFile, baseDir, overallLength)

    def more_to_do_query(self):
        """
        Called by other functions in order to provide an interface for users to
        continue to download files or to exit.
        """
        moreDownloads = self.query_response('Do you want to download more files?(y/n): ')
        if moreDownloads == 'n':
            print('Until next time!')
            return clean_exit()
        elif moreDownloads == 'y':
            print('Re-routing...')
            return InfoGather().file_loop_check()
        else:
            print('Something bad happened, please report this error to the creator.')
            return clean_exit()

    def csv_download_work(self, csvFile, baseDir, overallLength):
        if not baseDir.endswith('/') and baseDir != '':
            baseDir += '/'
        with open(csvFile, newline='') as csvfile:
            spreadsheet = csv.reader(csvfile, delimiter=',', quotechar='|')
            nl = 0
            for row in spreadsheet:
                nl += 1
            cl = 0
            widgets = ['Overall Progress: ', Percentage(), ' ',
                       Bar(marker='>', left='[', right=']'),
                       ' ', ETA(), ' ', FileTransferSpeed()]
            pbar = ProgressBar(widgets=widgets, maxval=overallLength)
            pbar.start()
            for row in spreadsheet:
                urlToGet = row[0]
                fileNameToSave = os.path.join(baseDir, urlToGet[urlToGet.rfind('/') + 1:])
                self.get_special_download(urlToGet, fileNameToSave)
                cl += 1
                pbar.update(overallLength / nl * cl)
                for i in range(overallLength):
                    pbar.update(i + 1)
            pbar.finish()
            note_set_and_send('Piddle: ', '%s download complete!' % fileNameToSave)
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
        widgets = ['Overall Progress: ', Percentage(), ' ',
                   Bar(marker='>', left='[', right=']'),
                   ' ', ETA(), ' ', FileTransferSpeed()]
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
        pbar.finish()
        print('All done!')
        note_set_and_send('Piddle: ', '%s download complete!' % fileNameToSave)
        return self.more_to_do_query()


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

    def csv_download_info(self):
        csvFile = input('Enter the CSV filename (with path) that contains the URLS (Q to quit): ')
        if csvFile.upper() == 'Q':
            return clean_exit()
        baseDir = input('Enter the directory path where you want the files saved (Q to quit): ')
        if baseDir.upper() == 'Q':
            return clean_exit()
        return self.work.get_csv_overall_length(csvFile, baseDir)

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
        elif specialDownload == 'y':
            response = self.work.query_response('Are you importing a CSV file?')
            if response == 'n':
                return self.reg_download_info()
            elif response == 'q':
                return clean_exit()
            else:
                return self.csv_download_info()
        return self.special_download_info()


def note_set_and_send(app, summary):
    """
    Creates a DBUS notification.
    """
    notify2.init('Piddle: ')
    return notify2.Notification(app, summary).show()


def clean_exit():
    """
    If we call this, we are exiting based on user input and not because of an
    error.
    """

    print("Thank you for using piddle.")
    exit(0)


def main():
    """
    Greets the user, requests and parses arguments, and calls relevant
    functions and methods.
    """
    VERSION = '0.3.dev'

    parser = argparse.ArgumentParser(description='pydl argument information.')
    parser.add_argument('-f', '--file', nargs='*',  action='append', dest='cFiles',
                        help='Given the full path,load each URL in the file. Also takes multiple file arguments.')
    parser.add_argument('-c', '--csv', nargs='*', action='append', dest='csvFiles',
                        help='Same as --file but specific to .csv files.')
    parser.add_argument('-d', '--dir',   nargs=1, action='store', default=".", dest='outputDir',
                        help='In a given directory check all files for URLs and download those.')
    parser.add_argument('-u', '--url', nargs='*', action='append', dest='cUrls',
                        help='This will grab 1-N urls. Use space as the delimitter.')
    parser.add_argument('-o', '--output', nargs=1,  action='store', dest='outputDir',
                        help='Move all downloaded files to this directory.')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s-' + VERSION,
                        help='Current version of pydl.py')

    ig = InfoGather()

    args = parser.parse_args()
    if args.cFiles:
        for file in args.cFiles:
            p = multiprocessing.Process(
                target=Workers().get_overall_length(fileNameUrls=file, baseDir=args.outputDir[0]))
            p.start()
    elif args.csvFiles:
        for file in args.csvFiles:
            p = multiprocessing.Process(
                target=Workers().get_csv_overall_length(csvFile=file, baseDir=args.outputDir[0]))
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