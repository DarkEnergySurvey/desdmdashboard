from monitor import pandas_utils
from monitor.models import Metric


def dashboard_home():

    metrics = Metric.objects.exclude(
            dashboard_display_option=Metric.DASHBOARD_DISPLAY_OPTION_NOSHOW).extra(
                    select={'lower_name': 'lower(name)'}).order_by('lower_name')

    sectiondict = {
            'title': 'Metrics Overview',
            'metric_listing': metrics,
            }

    return sectiondict

