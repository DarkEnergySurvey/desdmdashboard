from django.contrib import admin

from monitor.models import Source, Metric, Instrument,\
        MetricDataInt, MetricDataChar, MetricDataFloat, MetricDataDatetimeGMT,\
        MetricDataTimeDelta 

class InstrumentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Instrument, InstrumentAdmin)

class SourceAdmin(admin.ModelAdmin):
    pass
admin.site.register(Source, SourceAdmin)

class MetricAdmin(admin.ModelAdmin):
    pass
admin.site.register(Metric, MetricAdmin)

class MetricDataIntAdmin(admin.ModelAdmin):
    pass
admin.site.register(MetricDataInt, MetricDataIntAdmin)

class MetricDataFloatAdmin(admin.ModelAdmin):
    pass
admin.site.register(MetricDataFloat, MetricDataFloatAdmin)

class MetricDataCharAdmin(admin.ModelAdmin):
    pass
admin.site.register(MetricDataChar, MetricDataCharAdmin)

class MetricDataDatetimeGMTAdmin(admin.ModelAdmin):
    pass
admin.site.register(MetricDataDatetimeGMT, MetricDataDatetimeGMTAdmin)

class MetricDataTimeDeltaAdmin(admin.ModelAdmin):
    pass
admin.site.register(MetricDataTimeDelta, MetricDataTimeDeltaAdmin)
