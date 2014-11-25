#!/bin/bash

# -----------------------------------------------------------------------------
#
# script to be run as cron job on desdash to 
# 
# regularly regenrate the monitor cache
#
#
# author: michael.graber@fhnw.ch
# -----------------------------------------------------------------------------



source /eeups/eups/desdm_eups_setup.sh

setup DASHBOARDSERVER
setup docutils
setup CoreUtils

export PYTHONPATH=/webapps/releases/current/desdmdashboard_server/:$PYTHONPATH

python /webapps/releases/current/desdmdashboard_server/manage.py refresh_cache --settings=desdmdashboard.settings.settings_desdash_production
