from __future__ import absolute_import

from django.shortcuts import render
from django.views.decorators.cache import cache_page
from .models import TracTicketMetric

@cache_page(60 * 10)
def index(request):
    metrics = TracTicketMetric.objects.filter(show_on_dashboard=True)
    metrics = metrics.order_by('name')
    latest = [m.data.select_related('metric').latest() for m in metrics]
    return render(request, 'dashboard/index.html', {'data': latest})