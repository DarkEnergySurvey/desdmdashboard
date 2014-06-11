
import pandas

from desdmdashboard_remote.senddata.functions import send_metric_value

deshist = pandas.io.api.read_csv('deshist.csv')


def send_to_desdmdashboard(deshist):

    for i in range(len(deshist)):
        jrow = deshist.irow(i).to_json()
        send_metric_value('deshist', jrow, value_type='json')

