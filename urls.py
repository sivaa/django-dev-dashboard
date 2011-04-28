from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url('^$',                   'dashboard.views.index',        name="dashboard-index"),
    url('^metric/(\d+).json$',  'dashboard.views.metric_json',  name="metric-json"),
    url(r'^admin/', include(admin.site.urls)),
)
