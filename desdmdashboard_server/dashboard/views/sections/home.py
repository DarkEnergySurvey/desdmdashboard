from monitor import pandas_utils
from monitor.models import Metric


def dashboard_home():

    metrics = Metric.objects.exclude(
            dashboard_display_option=Metric.DASHBOARD_DISPLAY_OPTION_NOSHOW)

    sectiondict = {
            'title': 'Metrics Overview',
            'metric_listing': metrics,
            }

    return sectiondict

