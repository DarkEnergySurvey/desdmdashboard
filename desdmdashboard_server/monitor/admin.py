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

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

class MetricDataFloatInline(admin.TabularInline):
    model = MetricDataFloat 
    fields = ('value', 'time', 'has_error', 'error_message', )
    readonly_fields = ('value', 'time', 'has_error', 'error_message', )
    ordering = ('-time', )
    extra = 0

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

class MetricDataCharInline(admin.TabularInline):
    model = MetricDataChar 
    fields = ('value', 'time', 'has_error', 'error_message', )
    readonly_fields = ('value', 'time', 'has_error', 'error_message', )
    ordering = ('-time', )
    extra = 0

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

class MetricDataDatetimeInline(admin.TabularInline):
    model = MetricDataDatetime 
    fields = ('value', 'time', 'has_error', 'error_message', )
    readonly_fields = ('value', 'time', 'has_error', 'error_message', )
    ordering = ('-time', )
    extra = 0

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

class MetricDataJSONInline(admin.TabularInline):
    model = MetricDataJSON
    fields = ('value', 'time', 'has_error', 'error_message', )
    readonly_fields = ('value', 'time', 'has_error', 'error_message', )
    ordering = ('-time', )
    extra = 0

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

class MetricAdmin(admin.ModelAdmin):

    def __init__(self, *args, **kwargs):
        super(MetricAdmin, self).__init__(*args, **kwargs)
        # select inlines dynamically here : HOW?
    
    fields = (
            ('name', 'owner', 'slug', ),
            ('doc', ),
            ('latest_value', 'latest_time', 'latest_tags', 'has_error',
                'error_message'),
            ('warning_if_no_value_after_seconds', ),
            ('unit', 'dashboard_display_option', ),
            ('value_type', ),
            ('alert_operator', 'alert_value', 'alert_triggered', ),
            ('expression_string', 'expression_evaluation'),
            ('dashboard_display_window_length_days', ),
            ('timestamp_modified', 'timestamp_created', ),
            )

    prepopulated_fields = {'slug': ('name', ), }
    
    search_fields = ('name', 'doc', 'latest_tags', )

    list_display = ( 'name', 'owner', 'dashboard_display_option', 'latest_value',
            'latest_time', 'has_error', 'alert_triggered')
    
    readonly_fields = ('alert_triggered', 'timestamp_modified',
            'timestamp_created', 'latest_time', 'latest_value', 'latest_tags',
            'has_error', 'error_message', 'expression_evaluation')
    
#   inlines = (MetricDataIntInline, MetricDataFloatInline,
#           MetricDataCharInline, MetricDataDatetimeInline,
#           MetricDataJSONInline, )

        
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
