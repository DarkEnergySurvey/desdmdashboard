'''
DESDMDASHBOARD DATA COLLECTION JOB SCRIPT

A python script to be executed on a regular basis for the collection of
timestamped data in the DESDMDASHBOARD.

All functions that are supposed to be executed when this file is run have to be
called in main().


:: Author :: michael.graber@fhnw.ch
'''

from ..collect_functions.destest import file_archive_info__sum_filesize__archive_name


def main():
    file_archive_info__sum_filesize__archive_name()

if __name__ == '__main__':
    main()
