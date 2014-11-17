from optparse import make_option
from django.core.management.base import BaseCommand, CommandError

from monitor.models import Metric
from monitor_cache.models import MetricCache

class Command(BaseCommand):
    #args = '<poll_id poll_id ...>'
    help = 'Recomputes the content of the monitor application cache.'

    option_list = BaseCommand.option_list + (
        make_option('--verbose',
            action='store_true',
            dest='verbose',
            default=False,
            help='verbose progress indication'),
        )

    def handle(self, *args, **options):
        for metric in Metric.objects.all():
            if options['verbose']:
                print 'updating cache for metric ', metric.name
            _ = MetricCache.create_or_update(metric)
