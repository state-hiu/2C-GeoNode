import django
django.setup()
import decimal
from geonode.layers.models import Layer
from geonode.base.models import ResourceBase
from geonode.layers.utils import create_thumbnail
from geonode.geoserver.helpers import *
import csv
import sys

def create_layer_thumbnail(layer):
    """
    Create a thumbnail with a GeoServer request.
    """
    layer_name = layer.typename.encode('utf-8')
    wms_version = '1.1.1'
    wms_format = 'image/png8'

    params = {
        'service': 'WMS',
        'version': wms_version,
        'request': 'GetMap',
        'layers': layer_name,
        'format': wms_format,
        'width': 200,
        'height': 150
    }

    check_bbox = False
    if None not in layer.bbox:
        if ((layer.bbox[2]-layer.bbox[0]>0.0002) or (layer.bbox[3]-layer.bbox[1]>0.0002)):
            params['bbox'] = layer.bbox_string
        else:
            params['bbox'] = "%s,%s,%s,%s" % (str(layer.bbox[2]-decimal.Decimal('0.01')), str(layer.bbox[3]-decimal.Decimal('0.01')), str(layer.bbox[0]+decimal.Decimal('0.01')), str(layer.bbox[1]+decimal.Decimal('0.01')))
        check_bbox = True

    p = "&".join("%s=%s" % item for item in params.items())

    thumbnail_remote_url = ogc_server_settings.PUBLIC_LOCATION + "wms?" + p
    thumbnail_create_url = ogc_server_settings.LOCATION + "wms?" + p

    create_thumbnail(layer, thumbnail_remote_url, thumbnail_create_url, ogc_client=http_client, overwrite=True, check_bbox=False)

with open(sys.argv[1], 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='"')
    for row in reader:
        try:
            layer = Layer.objects.get(name=row[0].lower())
            create_layer_thumbnail(layer)
            print "[SUCESS] Layer [%s] thumbnail created" % (layer.name)
        except:
            print "[ERROR] Layer [%s] thumbnail couldn't be created" % (layer.name)
