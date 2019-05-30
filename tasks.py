import ast
import json
import logging
import os
import re


from invoke import run, task

BOOTSTRAP_IMAGE_CHEIP = 'codenvy/che-ip:nightly'


@task
def waitfordbs(ctx):
    print "**************************databases*******************************"
    ctx.run("./wait-for-databases.sh {0}".format('db'), pty=True)


@task
def update(ctx):
    print "***************************initial*********************************"
    ctx.run("env", pty=True)
    pub_ip = _geonode_public_host_ip()
    print "Public Hostname or IP is {0}".format(pub_ip)
    pub_port = _geonode_public_port()
    print "Public PORT is {0}".format(pub_port)
    db_url = _update_db_connstring()
    geodb_url = _update_geodb_connstring()
    override_env = "$HOME/.override_env"
    envs = {
        "public_fqdn": "{0}:{1}".format(pub_ip, pub_port or 80),
        "public_host": "{0}".format(pub_ip),
        "dburl": db_url,
        "geodburl": geodb_url,
        "override_fn": override_env
    }
    if not os.environ.get('GEOSERVER_PUBLIC_LOCATION'):
        ctx.run("echo export GEOSERVER_PUBLIC_LOCATION=\
http://{public_fqdn}/gs/ >> {override_fn}".format(**envs), pty=True)
    if not os.environ.get('SITEURL'):
        ctx.run("echo export SITEURL=\
http://{public_fqdn}/ >> {override_fn}".format(**envs), pty=True)

    try:
        current_allowed = ast.literal_eval(os.getenv('ALLOWED_HOSTS') or \
                                           "['{public_fqdn}', '{public_host}', 'localhost', 'django', 'sc',]".format(**envs))
    except ValueError:
        current_allowed = []
    current_allowed.extend(['{}'.format(pub_ip), '{}:{}'.format(pub_ip, pub_port)])
    allowed_hosts = ['"{}"'.format(c) for c in current_allowed] + ['"geonode"', '"django"']

    ctx.run('echo export ALLOWED_HOSTS="\\"{}\\"" >> {}'.format(allowed_hosts, override_env), pty=True)

    if not os.environ.get('DATABASE_URL'):
        ctx.run("echo export DATABASE_URL=\
{dburl} >> {override_fn}".format(**envs), pty=True)
    if not os.environ.get('GEODATABASE_URL'):
        ctx.run("echo export GEODATABASE_URL=\
{geodburl} >> {override_fn}".format(**envs), pty=True)
    if not os.environ.get('ASYNC_SIGNALS'):
        ctx.run("echo export ASYNC_SIGNALS=\
True >> {override_fn}".format(**envs), pty=True)
    if not os.environ.get('BROKER_URL'):
        ctx.run("echo export BROKER_URL=\
amqp://guest:guest@rabbitmq:5672/ >> {override_fn}".format(**envs), pty=True)
    ctx.run("source $HOME/.override_env", pty=True)
    print "****************************final**********************************"
    ctx.run("env", pty=True)


@task
def migrations(ctx):
    print "**************************migrations*******************************"
    ctx.run("python manage.py makemigrations --noinput --merge --settings={0}".format(
        _localsettings()
    ), pty=True)
    ctx.run("python manage.py makemigrations --noinput --settings={0}".format(
        _localsettings()
    ), pty=True)
    ctx.run("python manage.py migrate --noinput --settings={0}".format(
        _localsettings()
    ), pty=True)
    ctx.run("python manage.py updategeoip --settings={0}".format(
        _localsettings()
    ), pty=True)
    try:
        ctx.run("python manage.py rebuild_index --noinput --settings={0}".format(
            _localsettings()
        ), pty=True)
    except:
        pass

@task
def statics(ctx):
    print "**************************migrations*******************************"
    ctx.run('mkdir -p /mnt/volumes/statics/{static,uploads}')
    ctx.run("python manage.py collectstatic --noinput --clear --settings={0}".format(
        _localsettings()
    ), pty=True)

@task
def prepare(ctx):
    print "**********************prepare fixture***************************"
    ctx.run("rm -rf /tmp/default_oauth_apps_docker.json", pty=True)
    _prepare_oauth_fixture()


@task
def fixtures(ctx):
    print "**************************fixtures********************************"
    ctx.run("python manage.py loaddata sample_admin \
--settings={0}".format(_localsettings()), pty=True)
    ctx.run("python manage.py loaddata /tmp/default_oauth_apps_docker.json \
--settings={0}".format(_localsettings()), pty=True)
    ctx.run("python manage.py loaddata /usr/src/geonode/geonode/base/fixtures/initial_data.json \
--settings={0}".format(_localsettings()), pty=True)
    ctx.run("python manage.py set_all_layers_alternate \
--settings={0}".format(_localsettings()), pty=True)
#    ctx.run("python manage.py loaddata fixtures/base.json \
#--settings={0}".format(_localsettings()), pty=True)
#    ctx.run("python manage.py loaddata fixtures/layers.json \
#--settings={0}".format(_localsettings()), pty=True)
#    ctx.run("python manage.py rebuild_index --noinput --settings={0}".format(
#            _localsettings()
#        ), pty=True)




@task
def initialized(ctx):
    print "**************************init file********************************"
    ctx.run('date > /mnt/volumes/statics/geonode_init.lock')


def _update_db_connstring():
    user = os.getenv('GEONODE_DATABASE', 'geonode')
    pwd = os.getenv('GEONODE_DATABASE_PASSWORD', 'geonode')
    dbname = os.getenv('GEONODE_DATABASE', 'geonode')
    connstr = 'postgres://{0}:{1}@db:5432/{2}'.format(
        user,
        pwd,
        dbname
    )
    return connstr


def _update_geodb_connstring():
    geouser = os.getenv('GEONODE_GEODATABASE', 'geonode_data')
    geopwd = os.getenv('GEONODE_GEODATABASE_PASSWORD', 'geonode_data')
    geodbname = os.getenv('GEONODE_GEODATABASE', 'geonode_data')
    geoconnstr = 'postgis://{0}:{1}@db:5432/{2}'.format(
        geouser,
        geopwd,
        geodbname
    )
    return geoconnstr


def _localsettings():
    settings = os.getenv('DJANGO_SETTINGS_MODULE', 'sc.settings')
    return settings


def _geonode_public_host_ip():
    gn_pub_hostip = os.getenv('GEONODE_LB_HOST_IP', 'localhost')
    return gn_pub_hostip


def _geonode_public_port():
    gn_pub_port = os.getenv('GEONODE_LB_PORT', '80')
    return gn_pub_port


def _prepare_oauth_fixture():
    pub_ip = _geonode_public_host_ip()
    print "Public Hostname or IP is {0}".format(pub_ip)
    pub_port = _geonode_public_port()
    print "Public PORT is {0}".format(pub_port)
    default_fixture = [
        {
            "model": "oauth2_provider.application",
            "pk": 1001,
            "fields": {
                "skip_authorization": True,
                "created": "2018-05-31T10:00:31.661Z",
                "updated": "2018-05-31T11:30:31.245Z",
                "algorithm": "RS256",
                "redirect_uris": "http://{0}:{1}/geoserver/index.html".format(
                    pub_ip, pub_port
                ),
                "name": "GeoServer",
                "authorization_grant_type": "authorization-code",
                "client_type": "confidential",
                "client_id": "Jrchz2oPY3akmzndmgUTYrs9gczlgoV20YPSvqaV",
                "client_secret": "\
rCnp5txobUo83EpQEblM8fVj3QT5zb5qRfxNsuPzCqZaiRyIoxM4jdgMiZKFfePBHYXCLd7B8NlkfDB\
Y9HKeIQPcy5Cp08KQNpRHQbjpLItDHv12GvkSeXp6OxaUETv3",
                "user": [
                    "admin"
                ]
            }
        }
    ]
    with open('/tmp/default_oauth_apps_docker.json', 'w') as fixturefile:
        json.dump(default_fixture, fixturefile)