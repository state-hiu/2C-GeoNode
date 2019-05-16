from __future__ import print_function
import os
import sys

from geonode.layers.models import Layer

create_vector="""
curl -u admin:geoserver -v -XPOST -H 'Content-type: text/xml' \\
      -d '<featureType>
          <name>%(name)s</name>
          <title>%(title)s</title>
          </featureType>' \\
      "https://2c.puerti.co/geoserver/rest/workspaces/geonode/datastores/state_2c_geonode/featuretypes"
"""
vectors = Layer.objects.filter(storeType='dataStore')
datos = (dict(name=c.name, title=c.title, x0=c.bbox_x0, x1=c.bbox_x1, y0=c.bbox_y0, y1=c.bbox_y1) for c in vectors)

with open("vector_commands.bash", 'w') as f:
  for d in datos:
    print(create_vector % d, file=f)
    print("## %(name)s " % d, file=f)
