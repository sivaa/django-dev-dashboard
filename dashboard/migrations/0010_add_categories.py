# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table('dashboard_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('position', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
        ))
        db.send_create_signal('dashboard', ['Category'])

        # Adding field 'JenkinsFailuresMetric.category'
        db.add_column('dashboard_jenkinsfailuresmetric', 'category',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dashboard.Category'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'JenkinsFailuresMetric.position'
        db.add_column('dashboard_jenkinsfailuresmetric', 'position',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1),
                      keep_default=False)

        # Adding field 'GithubItemCountMetric.category'
        db.add_column('dashboard_githubitemcountmetric', 'category',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dashboard.Category'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'GithubItemCountMetric.position'
        db.add_column('dashboard_githubitemcountmetric', 'position',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1),
                      keep_default=False)

        # Adding field 'RSSFeedMetric.category'
        db.add_column('dashboard_rssfeedmetric', 'category',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dashboard.Category'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'RSSFeedMetric.position'
        db.add_column('dashboard_rssfeedmetric', 'position',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1),
                      keep_default=False)

        # Adding field 'TracTicketMetric.category'
        db.add_column('dashboard_tracticketmetric', 'category',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dashboard.Category'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'TracTicketMetric.position'
        db.add_column('dashboard_tracticketmetric', 'position',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table('dashboard_category')

        # Deleting field 'JenkinsFailuresMetric.category'
        db.delete_column('dashboard_jenkinsfailuresmetric', 'category_id')

        # Deleting field 'JenkinsFailuresMetric.position'
        db.delete_column('dashboard_jenkinsfailuresmetric', 'position')

        # Deleting field 'GithubItemCountMetric.category'
        db.delete_column('dashboard_githubitemcountmetric', 'category_id')

        # Deleting field 'GithubItemCountMetric.position'
        db.delete_column('dashboard_githubitemcountmetric', 'position')

        # Deleting field 'RSSFeedMetric.category'
        db.delete_column('dashboard_rssfeedmetric', 'category_id')

        # Deleting field 'RSSFeedMetric.position'
        db.delete_column('dashboard_rssfeedmetric', 'position')

        # Deleting field 'TracTicketMetric.category'
        db.delete_column('dashboard_tracticketmetric', 'category_id')

        # Deleting field 'TracTicketMetric.position'
        db.delete_column('dashboard_tracticketmetric', 'position')

    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'dashboard.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'})
        },
        'dashboard.datum': {
            'Meta': {'ordering': "['-timestamp']", 'object_name': 'Datum'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'measurement': ('django.db.models.fields.BigIntegerField', [], {}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        'dashboard.githubitemcountmetric': {
            'Meta': {'object_name': 'GithubItemCountMetric'},
            'api_url': ('django.db.models.fields.URLField', [], {'max_length': '1000'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dashboard.Category']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_url': ('django.db.models.fields.URLField', [], {'max_length': '1000'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'period': ('django.db.models.fields.CharField', [], {'default': "'instant'", 'max_length': '15'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'show_on_dashboard': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'show_sparkline': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'unit_plural': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'dashboard.jenkinsfailuresmetric': {
            'Meta': {'object_name': 'JenkinsFailuresMetric'},
            'build_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dashboard.Category']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_percentage': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_success_cnt': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'jenkins_root_url': ('django.db.models.fields.URLField', [], {'max_length': '1000'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'period': ('django.db.models.fields.CharField', [], {'default': "'instant'", 'max_length': '15'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'show_on_dashboard': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'show_sparkline': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'unit_plural': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'dashboard.rssfeedmetric': {
            'Meta': {'object_name': 'RSSFeedMetric'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dashboard.Category']", 'null': 'True', 'blank': 'True'}),
            'feed_url': ('django.db.models.fields.URLField', [], {'max_length': '1000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_url': ('django.db.models.fields.URLField', [], {'max_length': '1000'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'period': ('django.db.models.fields.CharField', [], {'default': "'instant'", 'max_length': '15'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'show_on_dashboard': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'show_sparkline': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'unit_plural': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'dashboard.tracticketmetric': {
            'Meta': {'object_name': 'TracTicketMetric'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dashboard.Category']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'period': ('django.db.models.fields.CharField', [], {'default': "'instant'", 'max_length': '15'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'query': ('django.db.models.fields.TextField', [], {}),
            'show_on_dashboard': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'show_sparkline': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'unit_plural': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['dashboard']