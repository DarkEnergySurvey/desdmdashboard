"""

Acquire Relevant metrics at the sytems level

"""
import subprocess
import sys 

from desdmdashboard_remote.senddata.decorators import Monitor
from desdmdashboard_collect.collect_utils import log

logger = log.get_logger('desdmdashboard_collect')

@Monitor('desar_httpd_cpu', value_type='int')
def sick_httpd() :
    """ Return the amount intergreted CPU by th emost cpu intensive httpd """

    out, err = commandline.shell_command(
            ("ps", "--no-headers", "-o" ,"cputime comm", "-A"))
    if err:
        logger.warning('sick_http aborted because of subprocess error.')
        raise commandline.DataCollectionCommandLineError(err)

    lines = out.rsplit('\n')

    #sanity -- put a 0 in have something that way if no httpd report 0
    cputimes=[0, ]
    for line in output.split('\n'):
        if debug: print >> sys.stderr, "Line:" ,line
        if not line :  continue
        (totalcpu, command) = line.split(' ', 1)
        if command!= "httpd" : continue
        # Grr arcane ascii format 
        # total format of totalCPU [ndays-]HH:MM:SS
        parts = totalcpu.split("-")
        if len(parts) == 2 :
            daysec=int(parts[0])*3600*24
            hhmmss=parts[1]
        elif len(parts) == 1:
            daysec=0
            hhmmss=parts[0]
        else:
            assert (False) # parse erros
        (hours, minutes, seconds) = hhmmss.split(":")
        total_seconds = daysec + int(hours)*3600 + int(minutes)*60 + int(seconds) 
        cputimes.append(total_seconds)
    cputimes.sort()
    maxtime = cputimes[-1]
    if debug : print >> sys.stderr, "max_httpd time", maxtime
    return maxtime
