from __future__ import absolute_import
import datetime
import time
from django import http
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from django.views.decorators.http import last_modified
from django.utils import simplejson
from .models import TracTicketMetric, Datum

@cache_page(60 * 10)
def index(request):
    data = []
    metrics = TracTicketMetric.objects.filter(show_on_dashboard=True).order_by('name')
    for metric in metrics:
        latest = metric.data.select_related('metric').latest()
        data.append({'metric': metric, 'latest': latest,})
    return render(request, 'dashboard/index.html', {'data': data})

def metric_last_modified(request, metric_id):
    try:
        return Datum.objects.filter(object_id=metric_id).latest().timestamp
    except Datum.DoesNotExist:
        return None

@cache_page(60 * 10)
@last_modified(metric_last_modified)
def metric_json(request, metric_id):
    metric = get_object_or_404(TracTicketMetric, pk=metric_id)
    
    one_month_ago = datetime.datetime.now() - datetime.timedelta(days=30)
    data = metric.data.filter(timestamp__gt=one_month_ago).order_by('timestamp')
    data = [(time.mktime(i.timestamp.timetuple()), i.measurement) for i in data]    
    return http.HttpResponse(
        simplejson.dumps(data, indent = 2 if settings.DEBUG else None),
        content_type = "application/json",
    )