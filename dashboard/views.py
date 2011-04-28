from __future__ import absolute_import
import datetime
import time
from django import http
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from django.utils import simplejson
from .models import TracTicketMetric

@cache_page(60 * 10)
def index(request):
    data = []
    metrics = TracTicketMetric.objects.filter(show_on_dashboard=True).order_by('name')
    for metric in metrics:
        latest = metric.data.select_related('metric').latest()
        data.append({'metric': metric, 'latest': latest})
    return render(request, 'dashboard/index.html', {'data': data})

@cache_page(60 * 10)
def metric_json(request, metric_id):
    metric = get_object_or_404(TracTicketMetric, pk=metric_id)
    
    one_month_ago = datetime.datetime.now() - datetime.timedelta(days=30)
    data = metric.data.filter(timestamp__gt=one_month_ago).order_by('timestamp')
    
    values = []
    timestamps = []
    for i in data:
        values.append(i.measurement)
        timestamps.append(time.mktime(i.timestamp.timetuple()))
    
    return http.HttpResponse(
        simplejson.dumps(
            {'values': values, 'timestamps': timestamps},
            indent = 2 if settings.DEBUG else None
        ),
        content_type = "application/json",
    )