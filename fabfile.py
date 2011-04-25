from fabric.api import *

def deploy():
    local('./manage.py collectstatic --noinput')
    local('epio upload')

def copydb():
    local('epio django -- dumpdata --natural dashboard > dddash.json')
    local('./manage.py loaddata dddash.json')