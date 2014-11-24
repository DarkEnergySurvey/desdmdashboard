from optparse import make_option
from django.core.management.base import BaseCommand, CommandError

from django.core.mail import EmailMessage

from django.conf import settings

from monitor.models import Metric
from monitor_cache.models import MetricCache


EMAIL_SUBJECT = "[desdmdashboard] !!! You're metric {metricname} is in TROUBLE !!"

EMAIL_CONTENT = '''

Hi {owner},

We observed that your metric {metricname} is in trouble.

The trouble message is:

{trouble_messages}


Here's a link to the metric: {url}

Cheers,
Michael
'''



class Command(BaseCommand):

    help = ('Sends emails about metrics in troubles to the metric owner and '
            'the dashboard admins.')

    option_list = BaseCommand.option_list + (
        make_option('--verbose',
            action='store_true',
            dest='verbose',
            default=False,
            help='verbose progress indication'),
        )

    def handle(self, *args, **options):
    
        for metric in Metric.objects.all():

            if metric.is_in_trouble_status and (metric.dashboard_display_option
                    != Metric.DASHBOARD_DISPLAY_OPTION_NOSHOW):

                adminemails = [adm[1] for adm in settings.ADMINS]

                mail = EmailMessage(
                        subject=EMAIL_SUBJECT.format(metricname=metric.name),
                        body=EMAIL_CONTENT.format(
                            metricname=metric.name,
                            owner=metric.owner.first_name,
                            trouble_messages='\n'.join(metric.get_trouble_statements()),
                            url=settings.DOMAIN_ROOT+metric.get_absolute_url()),
                        to=(metric.owner.email,),
                        cc=adminemails,
                        )

                mail.send()

                if options['verbose']:

                    print
                    print '------------------------------------------------------------------'
                    print EMAIL_SUBJECT.format(metricname=metric.name)
                    print '------------------------------------------------------------------'
                    print EMAIL_CONTENT.format(metricname=metric.name,
                                owner=metric.owner.first_name,
                                trouble_messages='\n'.join(metric.get_trouble_statements()),
                                url=settings.DOMAIN_ROOT+metric.get_absolute_url()),
                    print '------------------------------------------------------------------'
                    print

