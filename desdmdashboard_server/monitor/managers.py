from django.db import models

from django_pandas.managers import DataFrameQuerySet, PassThroughManager


class MetricManager(models.Manager):

    def get_by_natural_key(self, owner, name):
        try:
            return self.get(owner=owner, name=name)        
        except ValueError:
            try:
                return self.get(owner__username=owner, name=name)        
            except:
                raise
        except:
            raise


class MetricDataManager(PassThroughManager):

    def get_by_natural_key(self, owner, name):
        try:
            return self.get(owner=owner, name=name)        
        except ValueError:
            try:
                return self.get(owner__username=owner, name=name)        
            except:
                raise
        except:
            raise

    def get_dataframe_queryset(self, owner, name):
        m = self.get_by_natural_key(owner, name)
        vtclass = m.value_type.model_class()
        return DataFrameQuerySet(vtclass).filter(metric=m)
