# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'RSSFeedMetric.unit'
        db.add_column('dashboard_rssfeedmetric', 'unit', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True), keep_default=False)

        # Adding field 'RSSFeedMetric.unit_plural'
        db.add_column('dashboard_rssfeedmetric', 'unit_plural', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True), keep_default=False)

        # Adding field 'TracTicketMetric.unit'
        db.add_column('dashboard_tracticketmetric', 'unit', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True), keep_default=False)

        # Adding field 'TracTicketMetric.unit_plural'
        db.add_column('dashboard_tracticketmetric', 'unit_plural', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'RSSFeedMetric.unit'
        db.delete_column('dashboard_rssfeedmetric', 'unit')

        # Deleting field 'RSSFeedMetric.unit_plural'
        db.delete_column('dashboard_rssfeedmetric', 'unit_plural')

        # Deleting field 'TracTicketMetric.unit'
        db.delete_column('dashboard_tracticketmetric', 'unit')

        # Deleting field 'TracTicketMetric.unit_plural'
        db.delete_column('dashboard_tracticketmetric', 'unit_plural')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'dashboard.datum': {
            'Meta': {'ordering': "['-timestamp']", 'object_name': 'Datum'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'measurement': ('django.db.models.fields.BigIntegerField', [], {}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        'dashboard.rssfeedmetric': {
            'Meta': {'object_name': 'RSSFeedMetric'},
            'feed_url': ('django.db.models.fields.URLField', [], {'max_length': '1000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_url': ('django.db.models.fields.URLField', [], {'max_length': '1000'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'period': ('django.db.models.fields.CharField', [], {'default': "'instant'", 'max_length': '15'}),
            'show_on_dashboard': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'show_sparkline': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'unit': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'unit_plural': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'})
        },
        'dashboard.tracticketmetric': {
            'Meta': {'object_name': 'TracTicketMetric'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'period': ('django.db.models.fields.CharField', [], {'default': "'instant'", 'max_length': '15'}),
            'query': ('django.db.models.fields.TextField', [], {}),
            'show_on_dashboard': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'show_sparkline': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'unit': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'unit_plural': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'})
        }
    }

    complete_apps = ['dashboard']
