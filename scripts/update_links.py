import django
django.setup()
from geonode.base.models import ResourceBase
from geonode.base.models import Link
from geonode.maps.models import Map
from geonode.layers.models import Layer, Style
from geonode.utils import designals, resignals

source_str="147.102.109.19"
target_str="2c.puerti.co"

print "Deactivating GeoNode Signals..."
designals()
print "...done!"

maps = Map.objects.all()
for map in maps:
    print "Checking Map[%s]" % (map)
    if map.thumbnail_url:
        map.thumbnail_url = map.thumbnail_url.replace(source_str, target_str)
    map_layers = map.layers
    for layer in map_layers:
        if layer.ows_url:
            original = layer.ows_url
            layer.ows_url = layer.ows_url.replace(source_str, target_str)
            print "Updated OWS URL from [%s] to [%s]" % (original, layer.ows_url)
        if layer.layer_params:
            layer.layer_params = layer.layer_params.replace(source_str, target_str)
            print "Updated Layer Params also for Layer [%s]" % (layer)
        layer.save()
    map.save()
    print "Updated Map[%s]" % (map)

layers = Layer.objects.all()

for layer in layers:
    print "Checking Layer[%s]" % (layer)
    if layer.thumbnail_url:
        original = layer.thumbnail_url
        layer.thumbnail_url = layer.thumbnail_url.replace(source_str, target_str)
        layer.save()
        print "Updated Thumbnail URL from [%s] to [%s]" % (original, layer.thumbnail_url)

styles = Style.objects.all()

for style in styles:
    print "Checking Style[%s]" % (style)
    if style.sld_url:
        original = style.sld_url
        style.sld_url = style.sld_url.replace(source_str, target_str)
        style.save()
        print "Updated SLD URL from [%s] to [%s]" % (original, style.sld_url)

links = Link.objects.all()

for link in links:
    print "Checking Link[%s]" % (link)
    if link.url:
        original = link.url
        link.url = link.url.replace(source_str, target_str)
        link.save()
        print "Updated URL from [%s] to [%s]" % (original, link.url)

resources = ResourceBase.objects.all()

for res in resources:
    print "Checking Resource[%s]" % (res)
    if res.metadata_xml:
        original = res.metadata_xml
        res.metadata_xml = res.metadata_xml.replace(source_str, target_str)
        res.save()
        print "Updated metadata XML"

#print "Updating links..."
#for link in Link.objects.all():
#    new_url = str(link.url).replace(source_str,target_str)
#    link.url = new_url
#    link.save()


#print "Updating Resources..."
#for res in ResourceBase.objects.all():
#    new_xml = res.metadata_xml.encode('utf-8').replace(source_str,target_str)
#    res.metadata_xml = new_xml
#    res.save()

print "Reactivating GeoNode Signals..."
resignals()
print "...done!"

