"""

Acquire Relevant metrics at the sytems level

"""
import subprocess
import sys 

from desdmdashboard_remote.senddata import decorators

from desdmdashboard_remote.senddata.decorators import Monitor
from desdmdashboard_collect.collect_utils import log

logger = log.get_logger('desdmdashboard_collect')

def wc_l(cmd) :
    import subprocess
    """ Return the number of lines on stdout for the command   """
    stdout, stderr = subprocess.Popen(cmd, shell="True", stdout=subprocess.PIPE).communicate()
    if stderr:
        logger.warning('archive to fnal error: %s ' %(stderr))
        raise commandline.DataCollectionCommandLineError(stderr)
    return int(stdout)

@decorators.Monitor('connections_to_stken', value_type='int', logger=logger)
def stken_connections() :
    cmd = "netstat -t | grep stken.*fnal | grep ESTABLISHED |  wc -l"
    return wc_l(cmd)
    """ Return number of connections to the STKEN systems at fermilab 
        Connections are normaly open when sending data to the disaster                                                                                             
        recovery store at FNAL.                                                                                                  
    """
    cmd = "netstat -t | grep stken.*fnal | grep ESTABLISHED |  wc -l"
    return wc_l(cmd)



