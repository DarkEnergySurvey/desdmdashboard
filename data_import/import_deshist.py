
import pandas

from desdmdashboard_remote.senddata.functions import send_metric_value

deshist = pandas.io.api.read_csv('deshist.csv')


def send_to_desdmdashboard(deshist):

    for i in range(len(deshist)):
        jrow = deshist.irow(i).to_json()
        request = send_metric_value('deshist', jrow, value_type='json')
        if request.error_status[0]:
            print request.error_status[1]


if __name__ == '__main__':

    send_to_desdmdashboard(deshist)
