#!/bin/bash

# -----------------------------------------------------------------------------
#
# script to be run as cron job on desdash to 
#
# monitor whether metrics cause troubles and send an email if
#
#
# author: michael.graber@fhnw.ch
# -----------------------------------------------------------------------------



source /eeups/eups/desdm_eups_setup.sh

setup DASHBOARDSERVER
setup docutils
setup CoreUtils
setup pygments

export PYTHONPATH=/webapps/releases/current/desdmdashboard_server/:$PYTHONPATH

python /webapps/releases/current/desdmdashboard_server/manage.py send_trouble_emails --settings=desdmdashboard.settings.settings_desdash_production
