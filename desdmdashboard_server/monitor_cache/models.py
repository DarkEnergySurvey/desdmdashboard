from django.db import models

from monitor.models import Metric

from .content_generators import create_svg_plot_for_metric

# Create your models here.

class MetricCache(models.Model):

    metric = models.ForeignKey(Metric, unique=True, related_name='cache')

    # figures
    current_dashboard_figure = models.TextField(blank=True, null=True)
    current_detail_figure = models.TextField(blank=True, null=True)

    @classmethod
    def create_or_update(cls, metric):
        # get the cache object for the metric first
        obj, created = cls.objects.get_or_create(metric=metric)
        if created:
            obj.save()
        obj.update_cache()

        return obj


    def update_cache(self):

        # PUT HERE THE FUNCTIONALITY THAT UPDATES THE CACHE

        try:
            self.current_dashboard_figure = create_svg_plot_for_metric(
                    self.metric, kind='dashboard')
        except Exception, e:
            self.current_dashboard_figure = e

        try:
            self.current_detail_figure = create_svg_plot_for_metric(
                    self.metric, kind='detail')
        except Exception, e:
            self.current_detail_figure = e

        self.save()
