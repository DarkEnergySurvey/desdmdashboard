'''
DESDMDASHBOARD DATA COLLECTION JOB SCRIPT

A python script to be executed on a regular basis for the collection of
timestamped data in the DESDMDASHBOARD.

All functions that are supposed to be executed when this file is run have to be
called in main().

SETTING UP A CRONJOB ::
    You can use the script collect_cron_job.sh to run a cronjob in the correct
    eups setup:

    -   $crontab -e
    -   edit the file that is being opened with 





:: Author :: michael.graber@fhnw.ch
'''

from collect_functions.destest import file_archive_info__sum_filesize__archive_name


def main():
    file_archive_info__sum_filesize__archive_name()

if __name__ == '__main__':
    main()
