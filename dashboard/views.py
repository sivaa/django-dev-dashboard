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
        data.append({'metric': metric, 'latest': latest,})
    return render(request, 'dashboard/index.html', {'data': data})

def metric_detail(request, metric_id):
    metric = get_object_or_404(TracTicketMetric, pk=metric_id)
    return render(request, 'dashboard/detail.html', {
        'metric': metric,
        'latest': metric.data.latest(),
    })

@cache_page(60 * 10)
def metric_json(request, metric_id):
    metric = get_object_or_404(TracTicketMetric, pk=metric_id)
    
    try:
        daysback = int(request.GET['days'])
    except (TypeError, KeyError):
        daysback = 30    
    d = datetime.datetime.now() - datetime.timedelta(days=daysback)
    
    data = metric.data.filter(timestamp__gt=d) \
                      .order_by('timestamp') \
                      .values_list('timestamp', 'measurement')
    data = [(time.mktime(t.timetuple()), m) for (t, m) in data]    
    return http.HttpResponse(
        simplejson.dumps(data, indent = 2 if settings.DEBUG else None),
        content_type = "application/json",
    )