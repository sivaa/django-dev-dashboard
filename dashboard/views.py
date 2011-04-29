from __future__ import absolute_import
import datetime
import operator
import time
from django import http
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from django.utils import simplejson
from .models import Metric

@cache_page(60 * 10)
def index(request):
    metrics = []
    for MC in Metric.__subclasses__():
        metrics.extend(MC.objects.filter(show_on_dashboard=True))
    metrics = sorted(metrics, key=operator.attrgetter('name'))
    
    data = []
    for metric in metrics:
        latest = metric.data.latest()
        data.append({'metric': metric, 'latest': latest,})
    return render(request, 'dashboard/index.html', {'data': data})

def metric_detail(request, metric_slug):
    metric = _find_metric(metric_slug)
    return render(request, 'dashboard/detail.html', {
        'metric': metric,
        'latest': metric.data.latest(),
    })

@cache_page(60 * 10)
def metric_json(request, metric_slug):
    metric = _find_metric(metric_slug)
    
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

def _find_metric(slug):
    for MC in Metric.__subclasses__():
        try:
            return MC.objects.get(slug=slug)
        except MC.DoesNotExist:
            continue
    raise http.Http404()