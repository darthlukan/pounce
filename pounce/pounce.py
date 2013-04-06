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

        widgets = self.widgets
        pbar = ProgressBar(widgets=widgets, maxval=filelen).start()

        fileNameToSave = os.path.join(fileNameToSave, urlToGetFile[urlToGetFile.rfind('/') + 1:])

        proc = multiprocessing.Process(target=self.download(urlToGetFile, fileNameToSave))
        proc.start()
        proc.join()

        for i in range(filelen):
            pbar.update(i + 1)
        pbar.finish()
        note_set_and_send('Pounce: ', '%s download complete!' % fileNameToSave)
        return clean_exit()

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
            proc = multiprocessing.Process(target=self.download(urlToGetFile, fileNameToSave))
            proc.start()
            proc.join()
            cl += 1
            pbar.update(overallLength / nl * cl)
            for i in range(overallLength):
                pbar.update(i + 1)
            note_set_and_send('Pounce: ', '%s download complete!' % fileNameToSave)
        pbar.finish()
        note_set_and_send('Pounce: ', 'All jobs completed!')
        return clean_exit()

    def download(self, urlToGetFile, baseDir):
        """
        Takes the individual links from the url/file input,
        downloads the object that the URL points to, and copies it to the output directory/file.

        returns the status of shutil.copyfileobj()
        """
        # Thanks to BlaXpirit via http://goo.gl/V910H
        with urlopen(urlToGetFile, timeout=60) as response, open(baseDir, 'wb') as out_file:
            return shutil.copyfileobj(response, out_file)


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
    VERSION = '1.1'

    parser = argparse.ArgumentParser(description='pounce argument information.')
    parser.add_argument('-f', '--file', nargs=1,  action='store', dest='file',
                        help='Given the full path,load each URL in the file.')
    parser.add_argument('-u', '--url', nargs=1, action='store', dest='url',
                        help='This will grab 1 url.')
    parser.add_argument('-o', '--output', nargs=1,  action='store', dest='outputDir',
                        help='Move all downloaded files to this directory.')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s-' + VERSION,
                        help='Current version of pounce.py')

    args = parser.parse_args()
    if args.file:
        for file in args.file:
            p = multiprocessing.Process(
                target=Workers().get_overall_length(fileNameUrls=file, baseDir=args.outputDir[0]))
            p.start()
            p.join()
    elif args.url:
        for url in args.url:
            p = multiprocessing.Process(
                target=Workers().get_reg_download(urlToGetFile=url, fileNameToSave=args.outputDir[0]))
            p.start()
            p.join()
    else:
        parser.print_help()
        clean_exit()

if __name__ == '__main__':
    main()