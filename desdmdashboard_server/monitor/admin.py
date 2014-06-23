from django.contrib import admin

from monitor.models import Metric, MetricDataInt, MetricDataChar,\
        MetricDataFloat, MetricDataDatetime, MetricDataJSON
#       MetricDataTimeDelta, Source, Instrument


class MetricDataIntInline(admin.TabularInline):
    model = MetricDataInt
    fields = ('value', 'time', 'has_error', 'error_message',)
    readonly_fields = ('value', 'time', 'has_error', 'error_message',)
    ordering = ('-time', )
    extra = 0

class MetricDataFloatInline(admin.TabularInline):
    model = MetricDataFloat 
    fields = ('value', 'time', 'has_error', 'error_message', )
    readonly_fields = ('value', 'time', 'has_error', 'error_message', )
    ordering = ('-time', )
    extra = 0

class MetricDataCharInline(admin.TabularInline):
    model = MetricDataChar 
    fields = ('value', 'time', 'has_error', 'error_message', )
    readonly_fields = ('value', 'time', 'has_error', 'error_message', )
    ordering = ('-time', )
    extra = 0

class MetricDataDatetimeInline(admin.TabularInline):
    model = MetricDataDatetime 
    fields = ('value', 'time', 'has_error', 'error_message', )
    readonly_fields = ('value', 'time', 'has_error', 'error_message', )
    ordering = ('-time', )
    extra = 0

class MetricDataJSONInline(admin.TabularInline):
    model = MetricDataJSON
    fields = ('value', 'time', 'has_error', 'error_message', )
    readonly_fields = ('value', 'time', 'has_error', 'error_message', )
    ordering = ('-time', )
    extra = 0

class MetricAdmin(admin.ModelAdmin):

    def __init__(self, *args, **kwargs):
        super(MetricAdmin, self).__init__(*args, **kwargs)
        # select inlines dynamically here : HOW?
    
    fields = (
            ('name', 'owner', 'slug', ),
            ('doc', ),
            ('latest_value', 'last_updated', 'latest_tags', 'has_error',
                'error_message'),
            ('warning_if_no_value_after_seconds', ),
            ('unit', 'show_on_dashboard', ),
            ('value_type', ),
            ('alert_operator', 'alert_value', 'alert_triggered', ),
            ('timestamp_modified', 'timestamp_created', ),
            )

    prepopulated_fields = {'slug': ('name', ), }
    
    search_fields = ('name', 'doc', 'latest_tags', )

    list_display = ( 'name', 'owner', 'latest_value', 'last_updated',
            'has_error', 'alert_triggered')
    
    readonly_fields = ('alert_triggered', 'timestamp_modified',
            'timestamp_created', 'last_updated', 'latest_value', 'latest_tags',
            'has_error', 'error_message', )
    

    inlines = (MetricDataIntInline, MetricDataFloatInline,
            MetricDataCharInline, MetricDataDatetimeInline,
            MetricDataJSONInline, )

        
admin.site.register(Metric, MetricAdmin)


class MetricDataIntAdmin(admin.ModelAdmin):

    fields = (
            ('metric', ), 
            ('value', 'time', ), 
            ('tags', ), 
            ('has_error', 'error_message', ), 
            )

    list_display = ('metric', 'value', 'time', 'has_error', )

    list_filter = ('has_error', 'metric', )

    readonly_fields = ('timestamp_modified', 'timestamp_created', )
    

admin.site.register(MetricDataInt, MetricDataIntAdmin)


class MetricDataFloatAdmin(admin.ModelAdmin):

    fields = (
            ('metric', ), 
            ('value', 'time', ), 
            ('tags', ), 
            ('has_error', 'error_message', ), 
            )

    list_display = ('metric', 'value', 'time', 'has_error', )

    list_filter = ('has_error', 'metric', )

    readonly_fields = ('timestamp_modified', 'timestamp_created', )

admin.site.register(MetricDataFloat, MetricDataFloatAdmin)


class MetricDataCharAdmin(admin.ModelAdmin):

    fields = (
            ('metric', ), 
            ('value', 'time', ), 
            ('tags', ), 
            ('has_error', 'error_message', ), 
            )

    list_display = ('metric', 'value', 'time', 'has_error', )

    list_filter = ('has_error', 'metric', )

    readonly_fields = ('timestamp_modified', 'timestamp_created', )

admin.site.register(MetricDataChar, MetricDataCharAdmin)


class MetricDataDatetimeAdmin(admin.ModelAdmin):

    fields = (
            ('metric', ), 
            ('value', 'time', ), 
            ('tags', ), 
            ('has_error', 'error_message', ), 
            )

    list_display = ('metric', 'value', 'time', 'has_error', )

    list_filter = ('has_error', 'metric', )

    readonly_fields = ('timestamp_modified', 'timestamp_created', )

admin.site.register(MetricDataDatetime, MetricDataDatetimeAdmin)


class MetricDataJSONAdmin(admin.ModelAdmin):

    fields = (
            ('metric', ), 
            ('value', 'time', ), 
            ('tags', ), 
            ('has_error', 'error_message', ), 
            )

    list_display = ('metric', 'value', 'time', 'has_error', )

    list_filter = ('has_error', 'metric', )

    readonly_fields = ('timestamp_modified', 'timestamp_created', )

admin.site.register(MetricDataJSON, MetricDataJSONAdmin)
