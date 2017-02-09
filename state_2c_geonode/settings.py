# -*- coding: utf-8 -*-

import os
import dj_database_url
import copy
from geonode.settings import *  # noqa
from geonode.settings import (
    MIDDLEWARE_CLASSES,
    STATICFILES_DIRS,
    INSTALLED_APPS,
    CELERY_IMPORTS,
    MAP_BASELAYERS,
    DATABASES,
    CATALOGUE
)


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")

SITEURL = os.getenv('SITEURL',"http://2c.terranodo.io/")
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
GEONODE_ROOT = os.path.abspath(os.path.dirname(geonode_path))
DEBUG = str2bool(os.getenv('DEBUG', 'True'))
TEMPLATE_DEBUG = str2bool(os.getenv('TEMPLATE_DEBUG', 'False'))
DEBUG_STATIC = str2bool(os.getenv('DEBUG_STATIC', 'False'))
SECRET_KEY = os.getenv('SECRET_KEY', "02u6ws_cep$^^+vea-th+b2yuyo+$rhg)v-x&mj!p1cyt9nk+!")
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///development.db')
DATABASES = {'default':dj_database_url.parse(DATABASE_URL, conn_max_age=600),}
MANAGERS = ADMINS = os.getenv('ADMINS', [])
TIME_ZONE = os.getenv('TIME_ZONE', "America/Chicago")
SITE_ID = int(os.getenv('SITE_ID', '1'))
USE_I18N = str2bool(os.getenv('USE_I18N', 'True'))
USE_L10N = str2bool(os.getenv('USE_I18N', 'True'))
LANGUAGE_CODE = os.getenv('LANGUAGE_CODE', "en-us")
MODELTRANSLATION_LANGUAGES = ['en', ]
MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'
MODELTRANSLATION_FALLBACK_LANGUAGES = ('en',)
MEDIA_ROOT = os.getenv('MEDIA_ROOT', os.path.join(PROJECT_ROOT, "uploaded"))
MEDIA_URL = os.getenv('MEDIA_URL',"/uploaded/")
LOCAL_MEDIA_URL = os.getenv('LOCAL_MEDIA_URL',"/uploaded/")
STATIC_ROOT = os.getenv('STATIC_ROOT',os.path.join(PROJECT_ROOT, "static_root"))
_DEFAULT_STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, "static"),
    os.path.join(GEONODE_ROOT, "static"),
]
_DEFAULT_STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)
STATICFILES_FINDERS = os.getenv('STATICFILES_FINDERS',_DEFAULT_STATICFILES_FINDERS)
_DEFAULT_TEMPLATE_LOADERS = [
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
]
TEMPLATE_LOADERS = os.getenv('TEMPLATE_LOADERS',_DEFAULT_TEMPLATE_LOADERS)
_DEFAULT_TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, "templates"),
    os.path.join(GEONODE_ROOT, "templates"),
)
TEMPLATE_DIRS = os.getenv('TEMPLATE_DIRS',_DEFAULT_TEMPLATE_DIRS)
_DEFAULT_LOCALE_PATHS = (
    os.path.join(PROJECT_ROOT, "locale"),
    os.path.join(GEONODE_ROOT, "locale"),
)
LOCALE_PATHS = os.getenv('LOCALE_PATHS',_DEFAULT_LOCALE_PATHS)
ROOT_URLCONF = os.getenv('ROOT_URLCONF','state_2c_geonode.urls')
LOGIN_URL = os.getenv('LOGIN_URL','/account/login/')
LOGOUT_URL = os.getenv('LOGOUT_URL','/account/logout/')
MAX_DOCUMENT_SIZE = int(os.getenv('MAX_DOCUMENT_SIZE ','2'))  # MB


INSTALLED_APPS = (
    'geonode',
    'geonode-client',
) + INSTALLED_APPS


ALT_OSM_BASEMAPS = os.environ.get('ALT_OSM_BASEMAPS', True)
CARTODB_BASEMAPS = os.environ.get('CARTODB_BASEMAPS', True)
STAMEN_BASEMAPS = os.environ.get('STAMEN_BASEMAPS', True)
THUNDERFOREST_BASEMAPS = os.environ.get('THUNDERFOREST_BASEMAPS', True)
MAPBOX_ACCESS_TOKEN = os.environ.get('MAPBOX_ACCESS_TOKEN', None)
BING_API_KEY = os.environ.get('BING_API_KEY', None)

_INIT_DEFAULT_LAYER_SOURCE = {
    "ptype":"gxp_wmscsource",
    "url":"/geoserver/wms",
    "restUrl": "/gs/rest"
}

DEFAULT_LAYER_SOURCE = os.getenv('DEFAULT_LAYER_SOURCE',_INIT_DEFAULT_LAYER_SOURCE)

MAP_BASELAYERS = [{
    "source": {"ptype": "gxp_osmsource"},
    "type": "OpenLayers.Layer.OSM",
    "name": "OpenStreetMap",
    "visibility": True,
    "fixed": True,
    "group": "background"
}]
#MAP_BASELAYERS[0]['source']['url'] = OGC_SERVER['default']['LOCATION'] + 'wms'

# define the urls after the settings are overridden
if 'geonode.geoserver' in INSTALLED_APPS:
    LOCAL_GEOSERVER = {
        "source": {
            "ptype": "gxp_wmscsource",
            "url": OGC_SERVER['default']['PUBLIC_LOCATION'] + "wms",
            "restUrl": "/gs/rest"
        }
    }
    baselayers = MAP_BASELAYERS
    MAP_BASELAYERS = [LOCAL_GEOSERVER]
    MAP_BASELAYERS.extend(baselayers)

# Add additional paths (as regular expressions) that don't require
# authentication.
AUTH_EXEMPT_URLS = ('/api/o/*', '/api/roles', '/api/adminRole', '/api/users',)

# A tuple of hosts the proxy can send requests to.
PROXY_ALLOWED_HOSTS = ()

# The proxy to use when making cross origin requests.
PROXY_URL = '/proxy/?url=' if DEBUG else None

LAYER_PREVIEW_LIBRARY = 'react'

# Require users to authenticate before using Geonode
LOCKDOWN_GEONODE = str2bool(os.getenv('LOCKDOWN_GEONODE', 'True'))

# Require users to authenticate before using Geonode
if LOCKDOWN_GEONODE:
    MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + \
        ('geonode.security.middleware.LoginRequiredMiddleware',)

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', ['localhost', ])

# There are 3 ways to override GeoNode settings:
# 1. Using environment variables, if your changes to GeoNode are minimal.
# 2. Creating a downstream project, if you are doing a lot of customization.
# 3. Override settings in a local_settings.py file, legacy.
# Load more settings from a file called local_settings.py if it exists
try:
    from local_settings import *  # noqa
except ImportError:
    pass
