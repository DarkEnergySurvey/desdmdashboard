'''
DESDMDASHBOARD DATA COLLECTION FUNCTIONS


:: Author :: michael.graber@fhnw.ch
'''

from desdmdashboard_remote.senddata import decorators 

from desdmdashboard_collect.collect_utils import log 
logg = log.get_logger('desdmdashboard_collect')

@decorators.Monitor('test', value_type='char', logger=logg)
def test_collect_function():
    '''
    '''
    logg.info('in test_collect_function')
    return 'test output'

if __name__ == '__main__':
    test_collect_function()
