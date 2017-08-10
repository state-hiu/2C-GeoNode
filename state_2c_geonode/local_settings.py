import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

SITEURL = "http://dev.secondarycities.geonode.state.gov"

DATABASES = {
    'default': {
         'ENGINE': 'django.db.backends.postgresql_psycopg2',
         'NAME': 'state_2c_geonode_app',
         'USER': 'state_2c_geonode',
         'PASSWORD': 'state_2c_geonode',
     },
    # vector datastore for uploads
    'state_2c_geonode' : {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'state_2c_geonode',
        'USER' : 'state_2c_geonode',
        'PASSWORD' : 'state_2c_geonode',
        'HOST' : 'localhost',
        'PORT' : 5432
    }
}

# OGC (WMS/WFS/WCS) Server Settings
OGC_SERVER = {
    'default' : {
        'BACKEND' : 'geonode.geoserver',
        'LOCATION' : 'http://localhost:8080/geoserver/',
        'LOGIN_ENDPOINT': 'j_spring_oauth2_geonode_login',
        'LOGOUT_ENDPOINT': 'j_spring_oauth2_geonode_logout',
        'PUBLIC_LOCATION' : 'http://dev.secondarycities.geonode.state.gov/geoserver/',
        'USER' : 'admin',
        'PASSWORD' : 'geoserver',
        'MAPFISH_PRINT_ENABLED' : True,
        'PRINT_NG_ENABLED' : True,
        'GEONODE_SECURITY_ENABLED' : True,
        'GEOGIG_ENABLED' : False,
        'WMST_ENABLED' : False,
        'BACKEND_WRITE_ENABLED': True,
        'WPS_ENABLED' : False,
        'LOG_FILE': '%s/geoserver/data/logs/geoserver.log' % os.path.abspath(os.path.join(PROJECT_ROOT, os.pardir)),
        # Set to name of database in DATABASES dictionary to enable
        'DATASTORE': 'state_2c_geonode', #'datastore',
    }
}

CATALOGUE = {
    'default': {
        'ENGINE': 'geonode.catalogue.backends.pycsw_local',
        'URL': '%scatalogue/csw' % SITEURL,
    }
}

MEDIA_ROOT = "/var/www/state_2c_geonode/uploaded"
STATIC_ROOT = "/var/www/state_2c_geonode/static"
