from django.db import models

from django_pandas.managers import DataFrameQuerySet


class MetricManager(models.Manager):

    def get_by_natural_key(self, name, owner):
        try:
            return self.get(name=name, owner=owner)        
        except ValueError:
            try:
                return self.get(name=name, owner__username=owner)        
            except:
                raise
        except:
            raise


class MetricDataManager(PassThroughManager):

    def get_by_natural_key(self, name, owner):
        try:
            return self.get(name=name, owner=owner)        
        except ValueError:
            try:
                return self.get(name=name, owner__username=owner)        
            except:
                raise
        except:
            raise

    def get_queryset(self, name, owner):
        m = self.get_by_natural_key(name, owner)
        vtclass = m.value_type.model_class()
        return DataFrameQuerySet(vtclass).filter(metric=m)
