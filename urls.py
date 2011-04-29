from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url('^$',                       'dashboard.views.index',            name="dashboard-index"),
    url('^metric/([\w-]+)/$',       'dashboard.views.metric_detail',    name="metric-detail"),
    url('^metric/([\w-]+).json$',   'dashboard.views.metric_json',      name="metric-json"),
    url(r'^admin/', include(admin.site.urls)),
)
