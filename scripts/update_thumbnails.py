import django
django.setup()
import decimal
from geonode.layers.models import Layer
from geonode.base.models import ResourceBase
from geonode.layers.utils import create_thumbnail
from geonode.geoserver.helpers import *

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

all_layers = Layer.objects.all()

for index, layer in enumerate(all_layers):
    print "[%s / %s] Creating thumbnail for [%s] ..." % ((index + 1), len(all_layers), layer.name)
    try:
        create_layer_thumbnail(layer)
    except:
        print "[ERROR] Thumbnail for layer [%s] couldn't be created" % (layer.name)
