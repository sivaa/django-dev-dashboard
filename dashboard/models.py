import datetime
import xmlrpclib
import feedparser
import calendar
from django.conf import settings
from django.contrib.contenttypes.generic import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models, connections

METRIC_PERIOD_INSTANT = 'instant'
METRIC_PERIOD_DAILY = 'daily'
METRIC_PERIOD_WEEKLY = 'weekly'
METRIC_PERIOD_CHOICES = (
    (METRIC_PERIOD_INSTANT, 'Instant'),
    (METRIC_PERIOD_DAILY, 'Daily'),
    (METRIC_PERIOD_WEEKLY, 'Weekly'),
)

class Metric(models.Model):
    name = models.CharField(max_length=300)
    slug = models.SlugField()
    data = GenericRelation('Datum')
    show_on_dashboard = models.BooleanField(default=True)
    show_sparkline = models.BooleanField(default=True)
    period = models.CharField(max_length=15, choices=METRIC_PERIOD_CHOICES, 
                              default=METRIC_PERIOD_INSTANT)
    unit = models.CharField(max_length=100)
    unit_plural = models.CharField(max_length=100)

    class Meta:
        abstract = True
        
    def __unicode__(self):
        return self.name
        
    @models.permalink
    def get_absolute_url(self):
        return ("metric-detail", [self.slug])
        
    def gather_data(self, since):
        """
        Gather all the data from this metric since a given date.
        
        Returns a list of (timestamp, value) tuples. The timestamp is a Unix
        timestamp, coverted from localtime to UTC.
        """
        if self.period == METRIC_PERIOD_INSTANT:
            return self._gather_data_instant(since)
        elif self.period == METRIC_PERIOD_DAILY:
            return self._gather_data_periodic(since, 'day')
        elif self.period == METRIC_PERIOD_WEEKLY:
            return self._gather_data_periodic(since, 'week')
        else:
            raise ValueError("Unknown period: %s", self.period)
    
    def _gather_data_instant(self, since):
        """
        Gather data from an "instant" metric.
        
        Instant metrics change every time we measure them, so they're easy:
        just return every single measurement.
        """
        data = self.data.filter(timestamp__gt=since) \
                        .order_by('timestamp') \
                        .values_list('timestamp', 'measurement')
        return [(calendar.timegm(t.timetuple()), m) for (t, m) in data]

    def _gather_data_periodic(self, since, period):
        """
        Gather data from "periodic" merics.
        
        Period metrics are reset every day/week/month and count up as the period
        goes on. Think "commits today" or "new tickets this week".
        
        XXX I'm not completely sure how to deal with this since time zones wreak
        havoc, so there's right now a hard-coded offset which doesn't really
        scale but works for now.
        """
        OFFSET = "2 hours" # HACK!
        ctid = ContentType.objects.get_for_model(self).id
        
        c = connections['default'].cursor()
        c.execute('''SELECT 
                        DATE_TRUNC(%s, timestamp - INTERVAL %s),
                        MAX(measurement)
                     FROM dashboard_datum
                     WHERE content_type_id = %s 
                       AND object_id = %s
                       AND timestamp >= %s
                     GROUP BY 1;''', [period, OFFSET, ctid, self.id, since])
        return [(calendar.timegm(t.timetuple()), float(m)) for (t, m) in c.fetchall()]

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