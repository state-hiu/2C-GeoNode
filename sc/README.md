# geonode-client [![Build Status](https://travis-ci.org/GeoNode/geonode-mapstore-client.svg?branch=master)](https://travis-ci.org/GeoNode/geonode-mapstore-client) [![Code Climate](https://codeclimate.com/github/GeoNode/geonode-viewer/badges/gpa.svg)](https://codeclimate.com/github/GeoNode/geonode-viewer) [![Test Coverage](https://codeclimate.com/github/GeoNode/geonode-mapstore-client/badges/coverage.svg)](https://codeclimate.com/github/GeoNode/geonode-mapstore-client/coverage)

MapStore - React map viewer for GeoNode

## Installation

Install `node` and `npm`. We would encourage you to use [nvm](https://github.com/creationix/nvm) a version manager for node.

You need `node > 5`

Run `npm install` to install all dependencies.

## Development Server

Run `npm start` to start the development server. Visit your browser at `http://localhost:8080` to see the result.

## Testing

During development run `npm run test:watch` to run tests on every file change.  

Run `npm test` to run the full test suite with code coverage report.  

## Building

- Building is done via webpack and the command is `npm build`  
- The dist folder is where the minified versions of these files are stored.  

## Deployment to GH-pages

Automated deployment via travis is enabled for the master branch.

If you want to deploy manually to gh-pages use `npm run deploy`

### Important
The deplyoment uses the `index-gh.html` please keep this file in sync with `index.html` and change the path once the repo changes it's name. The `.travis.yml` needs to be changed as well.

## Integrating into GeoNode/Django

- Execute `pip install django-mapstore-adapter --upgrade`
- Execute `pip install django-geonode-mapstore-client --upgrade`

### GeoNode settings update
Update your `GeoNode` > `settings.py` as follows:

```
# To enable the MapStore2 based Client enable those
if 'geonode_mapstore_client' not in INSTALLED_APPS:
    INSTALLED_APPS += (
        'mapstore2_adapter',
        'geonode_mapstore_client',)

GEONODE_CLIENT_LAYER_PREVIEW_LIBRARY = 'mapstore'  # DEPRECATED use HOOKSET instead
GEONODE_CLIENT_HOOKSET = "geonode_mapstore_client.hooksets.MapStoreHookSet"

MAPSTORE_DEBUG = False

def get_geonode_catalogue_service():
    if PYCSW:
        pycsw_config = PYCSW["CONFIGURATION"]
        if pycsw_config:
                pycsw_catalogue = {
                    ("%s" % pycsw_config['metadata:main']['identification_title']): {
                        "url": CATALOGUE['default']['URL'],
                        "type": "csw",
                        "title": pycsw_config['metadata:main']['identification_title'],
                        "autoload": True
                     }
                }
                return pycsw_catalogue
    return None

GEONODE_CATALOGUE_SERVICE = get_geonode_catalogue_service()

MAPSTORE_CATALOGUE_SERVICES = {
    "Demo WMS Service": {
        "url": "https://demo.geo-solutions.it/geoserver/wms",
        "type": "wms",
        "title": "Demo WMS Service",
        "autoload": False
     },
    "Demo WMTS Service": {
        "url": "https://demo.geo-solutions.it/geoserver/gwc/service/wmts",
        "type": "wmts",
        "title": "Demo WMTS Service",
        "autoload": False
    }
}

MAPSTORE_CATALOGUE_SELECTED_SERVICE = "Demo WMS Service"

if GEONODE_CATALOGUE_SERVICE:
    MAPSTORE_CATALOGUE_SERVICES[GEONODE_CATALOGUE_SERVICE.keys()[0]] = GEONODE_CATALOGUE_SERVICE[GEONODE_CATALOGUE_SERVICE.keys()[0]]
    MAPSTORE_CATALOGUE_SELECTED_SERVICE = GEONODE_CATALOGUE_SERVICE.keys()[0]

DEFAULT_MS2_BACKGROUNDS = [{
        "type": "osm",
        "title": "Open Street Map",
        "name": "mapnik",
        "source": "osm",
        "group": "background",
        "visibility": True
    },
    {
        "group": "background",
        "name": "osm",
        "source": "mapquest",
        "title": "MapQuest OSM",
        "type": "mapquest",
        "visibility": False
    }
]

MAPSTORE_BASELAYERS = DEFAULT_MS2_BACKGROUNDS

if 'geonode.geoserver' in INSTALLED_APPS:
    LOCAL_GEOSERVER = {
        "type": "wms",
        "url": OGC_SERVER['default']['PUBLIC_LOCATION'] + "wms",
        "visibility": True,
        "title": "Local GeoServer",
        "group": "background",
        "format": "image/png8",
        "restUrl": "/gs/rest"
    }
```

### Update migrations and static files

- Execute `DJANGO_SETTINGS_MODULE=<your_geonode.settings> python manage.py migrate`
- Execute `DJANGO_SETTINGS_MODULE=<your_geonode.settings> python manage.py collectstatic`
