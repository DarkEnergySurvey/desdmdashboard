#!/bin/sh

source /work/apps/RHEL6/dist/eups/desdm_eups_setup.sh
export EUPS_PATH=$EUPS_PATH:/work/users/mgower/my_eups_prods

setup FWRefact mmgtrunk
export DES_DB_SECTION=db-oracle-newtest

#deshist --cols=run,status,operator,blkcnt,lastblk,target_site,pipever,starttime,wallclock,endtime --section=db-oracle-newtest --startdate 05/01/2014,06/01/2014
sd=`date --date="-14 day" +%x`
ed=`date --date="+1 day" +%x`
deshist --format=csv --cols=basket,run,status,operator,blkcnt,lastblk,lastmod-l,lastmod-h,target_site,pipever,starttime,wallclock,endtime --section=db-oracle-newtest --startdate $sd,$ed > /home/mgower/cron_deshist/deshist.csv
