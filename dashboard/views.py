from __future__ import absolute_import
import datetime
from time import mktime
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.utils import simplejson
from .models import TracTicketMetric

@cache_page(60 * 10)
def index(request):
    data= []
    one_month_ago = datetime.datetime.now() - datetime.timedelta(days=30)
    metrics = TracTicketMetric.objects.all().order_by('name')
    for metric in metrics :
        latest = metric.data.select_related('metric').latest()
        data_list = list(metric.data.filter(timestamp__gt=one_month_ago).order_by('timestamp'))
        thirty_days_values = [datum.measurement for datum in data_list]
        thirty_days_timestamps= [mktime(datum.timestamp.timetuple())+1e-6*datum.timestamp.microsecond for datum in data_list]
        report={
            'latest':latest,
            'thirty_days_values':simplejson.dumps(thirty_days_values),
            'thirty_days_timestamps':simplejson.dumps(thirty_days_timestamps),
            'first_stamp':data_list[0].timestamp,
            'last_stamp':data_list[-1].timestamp,
        }
        data.append(report)

    return render(request, 'dashboard/index.html', {'data': data})