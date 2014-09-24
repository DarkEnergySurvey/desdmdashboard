from django.db import models

from monitor.models import Metric

from .content_generators import create_svg_plot_for_metric

# Create your models here.

class MetricCache(models.Model):

    metric = models.ForeignKey(Metric, unique=True)

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


    def update_cache(self):

        # PUT HERE THE FUNCTIONALITY THAT UPDATES THE CACHE

        self.current_dashboard_figure = create_svg_plot_for_metric(self.metric,
                kind='dashboard')
        self.current_detail_figure = create_svg_plot_for_metric(self.metric,
                kind='detail')

        self.save()