from __future__ import print_function
import os
import sys

from geonode.layers.models import Layer

create_store = """
curl -u admin:geoserver -v -XPOST -H 'Content-type: text/xml' \
     -d '<coverageStore>
         <name>%(name)s</name>
         <workspace>geonode</workspace>
         <enabled>true</enabled>
         <type>GeoTIFF</type>
         <url>/geoserver_data/data/geonode/%(name)s.tif</url>
         </coverageStore>' \
     "http://localhost:8080/geoserver/rest/workspaces/geonode/coveragestores?configure=all"
"""

create_coverage="""
curl -u admin:geoserver -v -XPOST -H 'Content-type: text/xml' \
      -d '<coverage>
          <name>%(name)s</name>
          <title>%(title)s</title>
          <nativeCRS>GEOGCS[&quot;WGS 84&quot;,DATUM[&quot;World Geodetic System 1984&quot;,SPHEROID[&quot;WGS 84&quot;,6378137.0, 298.257223563, AUTHORITY[&quot;EPSG&quot;,&quot;7030&quot;]],AUTHORITY[&quot;EPSG&quot;,&quot;6326&quot;]],PRIMEM[&quot;Greenwich&quot;, 0.0, AUTHORITY[&quot;EPSG&quot;,&quot;8901&quot;]],UNIT[&quot;degree&quot;, 0.017453292519943295],AXIS[&quot;Geodetic longitude&quot;, EAST],AXIS[&quot;Geodetic latitude&quot;, NORTH],AUTHORITY[&quot;EPSG&quot;,&quot;4326&quot;]]</nativeCRS>
          <srs>EPSG:4326</srs>
          <latLonBoundingBox><minx>%(x0)f</minx><maxx>%(x1)f</maxx><miny>%(y0)f</miny><maxy>%(y1)f</maxy><crs>EPSG:4326</crs></latLonBoundingBox>
          </coverage>' \
      "http://localhost:8080/geoserver/rest/workspaces/geonode/coveragestores/%(name)s/coverages"
"""
coverages = Layer.objects.filter(storeType='coverageStore')
datos = (dict(name=c.name, title=c.title, x0=c.bbox_x0, x1=c.bbox_x1, y0=c.bbox_y0, y1=c.bbox_y1) for c in coverages)

with open("coverage_commands.bash", 'w') as f:
  for d in datos:
    print(create_store % d, file=f)
    print(create_coverage % d, file=f)
    print("## %(name)s " % d, file=f)
