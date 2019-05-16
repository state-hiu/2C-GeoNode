from __future__ import print_function
import os
import sys

from geonode.layers.models import Layer

connect_style="""
      curl -u admin:geoserver -v -XPUT -H 'Content-Type:text/xml' -d '<layer><defaultStyle><workspace>geonode</workspace><name>%(name)s</name></defaultStyle><enabled>true</enabled><advertised>false</advertised></layer>' https://2c.puerti.co/geoserver/rest/layers/geonode:%(name)s
"""
layers = Layer.objects.all()
datos = (dict(name=c.name, title=c.title, x0=c.bbox_x0, x1=c.bbox_x1, y0=c.bbox_y0, y1=c.bbox_y1) for c in layers)

with open("style_commands.bash", 'w') as f:
  for d in datos:
    print(connect_style % d, file=f)
    print("## %(name)s " % d, file=f)
