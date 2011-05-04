from fabric.api import *

def deploy():
    local('./manage.py collectstatic --noinput')
    local('epio upload')

def copydb():
    local('epio django -- dumpdata --natural dashboard | gzip '
          '> dashboard/fixtures/example_data.json.gz')
    local('./manage.py loaddata dashboard/fixtures/example_data.json.gz')