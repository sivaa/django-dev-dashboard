from __future__ import absolute_import

from django.contrib import admin
from .models import Metric, Datum

class MetricAdmin(admin.ModelAdmin):
    list_display = ('name', 'show_on_dashboard', 'show_sparkline')
    list_editable = ('show_on_dashboard', 'show_sparkline')
    prepopulated_fields = {'slug': ['name']}

for MC in Metric.__subclasses__():
    admin.site.register(MC, MetricAdmin)

admin.site.register(Datum, 
    list_display = ('timestamp', 'metric', 'measurement'),
)