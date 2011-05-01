import datetime
import urllib
import xmlrpclib
import feedparser
from django.conf import settings
from django.contrib.contenttypes.generic import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models

METRIC_PERIOD_INSTANT = 'instant'
METRIC_PERIOD_DAILY = 'daily'
METRIC_PERIOD_CHOICES = (
    (METRIC_PERIOD_INSTANT, 'Instant'),
    (METRIC_PERIOD_DAILY, 'Daily'),
)

class Metric(models.Model):
    name = models.CharField(max_length=300)
    slug = models.SlugField()
    data = GenericRelation('Datum')
    show_on_dashboard = models.BooleanField(default=True)
    show_sparkline = models.BooleanField(default=True)
    period = models.CharField(max_length=15, choices=METRIC_PERIOD_CHOICES, 
                              default=METRIC_PERIOD_INSTANT)

    class Meta:
        abstract = True
        
    def __unicode__(self):
        return self.name
        
    @models.permalink
    def get_absolute_url(self):
        return ("metric-detail", [self.pk])

class TracTicketMetric(Metric):
    query = models.TextField()
    
    def __unicode__(self):
        return self.name
    
    def fetch(self):
        s = xmlrpclib.ServerProxy(settings.TRAC_RPC_URL)
        return len(s.ticket.query(self.query + "&max=0"))
    
    def link(self):
        return "%squery?%s" % (settings.TRAC_URL, self.query)

class RSSFeedMetric(Metric):
    feed_url = models.URLField(max_length=1000)
    link_url = models.URLField(max_length=1000)
    
    def fetch(self):
        return len(feedparser.parse(self.feed_url).entries)
    
    def link(self):
        return self.link_url

class Datum(models.Model):
    metric = GenericForeignKey()
    content_type = models.ForeignKey(ContentType, related_name='+')
    object_id = models.PositiveIntegerField()
    timestamp = models.DateTimeField(default=datetime.datetime.now)
    measurement = models.BigIntegerField()
    
    class Meta:
        ordering = ['-timestamp']
        get_latest_by = 'timestamp'
        verbose_name_plural = 'data'
        
    def __unicode__(self):
        return "%s at %s: %s" % (self.metric, self.timestamp, self.measurement)