#!/bin/bash

# -----------------------------------------------------------------------------
#
# script to be run as cron job on desdash to 
#
# monitor whether a metrics cause troubles
#
#
# author: michael.graber@fhnw.ch
# -----------------------------------------------------------------------------



source /eeups/eups/desdm_eups_setup.sh

setup DASHBOARDSERVER
setup docutils
setup CoreUtils

export PYTHONPATH=$PYTHONPATH:/webapps/releases/current/desdmdashboard_server/

python /webapps/releases/current/desdmdashboard_server/manage.py send_trouble_emails --settings=desdmdashboard.settings.settings_desdash_production
