'''
DESDMDASHBOARD DATA COLLECTION FUNCTIONS


:: Author :: michael.graber@fhnw.ch
'''

from desdmdashboard_remote.senddata import decorators 

from desdmdashboard_collect.collect_utils import log 
logg = log.get_logger('desdmdashboard_collect')

@decorators.Monitor('test', value_type='int', logger=logg)
def test_collect_function():
    '''
    My test docu
    <<<<<<<<<<<<

    section 1
    ~~~~~~~~~
    Now we even have a section

    - and
    - believe it
    - or not

    a **list** and *bold* and *italic* print.

    '''
    logg.info('in test_collect_function')
    return 10

if __name__ == '__main__':
    test_collect_function()
