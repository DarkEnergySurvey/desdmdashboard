from django.db import models
from django.db.models.query import QuerySet
from .io import read_frame


# the PassThroughManager code is freely taken from the django-model-utils
# package, specifically from
# https://github.com/carljm/django-model-utils/blob/master/model_utils/managers.py


class PassThroughManagerMixin(object):
    """
    A mixin that enables you to call custom QuerySet methods from your manager.
    """

    # pickling causes recursion errors
    _deny_methods = ['__getstate__', '__setstate__', '__getinitargs__',
                     '__getnewargs__', '__copy__', '__deepcopy__', '_db',
                     '__slots__']

    def __init__(self, queryset_cls=None):
        self._queryset_cls = queryset_cls
        super(PassThroughManagerMixin, self).__init__()

    def __getattr__(self, name):
        if name in self._deny_methods:
            raise AttributeError(name)
        if django.VERSION < (1, 6, 0):
            return getattr(self.get_query_set(), name)
        return getattr(self.get_queryset(), name)

    def get_queryset(self):
        try:
            qs = super(PassThroughManagerMixin, self).get_queryset()
        except AttributeError:
            qs = super(PassThroughManagerMixin, self).get_query_set()
        if self._queryset_cls is not None:
            qs = qs._clone(klass=self._queryset_cls)
        return qs

    get_query_set = get_queryset

    @classmethod
    def for_queryset_class(cls, queryset_cls):
        return create_pass_through_manager_for_queryset_class(cls, queryset_cls)


class PassThroughManager(PassThroughManagerMixin, models.Manager):
    """
    Inherit from this Manager to enable you to call any methods from your
    custom QuerySet class from your manager. Simply define your QuerySet
    class, and return an instance of it from your manager's `get_queryset`
    method.

    Alternately, if you don't need any extra methods on your manager that
    aren't on your QuerySet, then just pass your QuerySet class to the
    ``for_queryset_class`` class method.

    class PostQuerySet(QuerySet):
        def enabled(self):
            return self.filter(disabled=False)

    class Post(models.Model):
        objects = PassThroughManager.for_queryset_class(PostQuerySet)()

    """
    pass


# this is standard django_pandas code

class DataFrameQuerySet(QuerySet):

    def to_pivot_table(self, fieldnames=(), verbose=True,
                       values=None, rows=None, cols=None,
                       aggfunc='mean', fill_value=None, margins=False,
                       dropna=True):
        """
        A convenience method for creating a spread sheet style pivot table
        as a DataFrame
        Parameters
        ----------
        fieldnames:  The model field names to utilise in creating the frame.
            to span a relationship, just use the field name of related
            fields across models, separated by double underscores,
        values : column to aggregate, optional
        rows : list of column names or arrays to group on
            Keys to group on the x-axis of the pivot table
        cols : list of column names or arrays to group on
            Keys to group on the y-axis of the pivot table
        aggfunc : function, default numpy.mean, or list of functions
            If list of functions passed, the resulting pivot table will have
            hierarchical columns whose top level are the function names
            (inferred from the function objects themselves)
        fill_value : scalar, default None
            Value to replace missing values with
        margins : boolean, default False
            Add all row / columns (e.g. for subtotal / grand totals)
        dropna : boolean, default True
        Do not include columns whose entries are all NaN
        """
        df = self.to_dataframe(fieldnames, verbose=verbose)

        return df.pivot_table(values=values, fill_value=fill_value, rows=rows,
                              cols=cols, aggfunc=aggfunc, margins=margins,
                              dropna=dropna)

    def to_timeseries(self, fieldnames=(), verbose=True,
                      index=None, storage='wide',
                      values=None, pivot_columns=None, freq=None,
                      rs_kwargs=None):
        """
        A convenience method for creating a time series i.e the
        DataFrame index is instance of a DateTime or PeriodIndex

        Parameters
        ----------

        fieldnames:  The model field names to utilise in creating the frame.
            to span a relationship, just use the field name of related
            fields across models, separated by double underscores,

        index: specify the field to use  for the index. If the index
            field is not in the field list it will be appended. This
            is mandatory.

        storage:  Specify if the queryset uses the `wide` or `long` format
            for data.

        pivot_column: Required once the you specify `long` format
            storage. This could either be a list or string identifying
            the field name or combination of field. If the pivot_column
            is a single column then the unique values in this column become
            a new columns in the DataFrame
            If the pivot column is a list the values in these columns are
            concatenated (using the '-' as a separator)
            and these values are used for the new timeseries columns

        values: Also required if you utilize the `long` storage the
            values column name is use for populating new frame values

        freq: the offset string or object representing a target conversion

        rs_kwargs: Arguments based on pandas.DataFrame.resample
        """
        if index is None:
            raise AssertionError('You must supply an index field')
        if storage not in ('wide', 'long'):
            raise AssertionError('storage must be wide or long')
        if rs_kwargs is None:
            rs_kwargs = {}

        if storage == 'wide':
            df = self.to_dataframe(fieldnames, verbose=verbose, index=index)
        else:
            df = self.to_dataframe(fieldnames, verbose=verbose)
            if values is None:
                raise AssertionError('You must specify a values field')

            if pivot_columns is None:
                raise AssertionError('You must specify pivot_columns')

            if isinstance(pivot_columns, (tuple, list)):
                df['combined_keys'] = ''
                for c in pivot_columns:
                    df['combined_keys'] += df[c].str.upper() + '.'

                df['combined_keys'] += values.lower()

                df = df.pivot(index=index,
                              columns='combined_keys',
                              values=values)
            else:
                df = df.pivot(index=index,
                              columns=pivot_columns,
                              values=values)

        if freq is not None:
            df = df.resample(freq, **rs_kwargs)

        return df

    def to_dataframe(self, fieldnames=(), verbose=True, index=None, fill_na=None,
                     coerce_float=False):
        """
        Returns a DataFrame from the queryset

        Paramaters
        -----------

        fieldnames:  The model fields to utilise in creating the frame.
            to span a relationship, just use the field name of related
            fields across models, separated by double underscores,


        index: specify the field to use  for the index. If the index
               field is not in the field list it will be appended

        fill_na: fill in missing observations using one of the following
                 this is a string  specifying a pandas fill method
                 {'backfill, 'bill', 'pad', 'ffill'} or a scalar value

        coerce_float: Attempt to convert the numeric non-string data
                like object, decimal etc. to float if possible
        """

        df = read_frame(self, fieldnames=fieldnames, verbose=verbose,
                        index_col=index,
                        coerce_float=coerce_float)

        if fill_na is not None:
            if fill_na not in ('backfill', 'bfill', 'pad', 'ffill'):
                df = df.fillna(value=fill_na)
            else:
                df = df.fillna(method=fill_na)

        return df


class DataFrameManager(PassThroughManager):
    def get_query_set(self):
        return DataFrameQuerySet(self.model)
