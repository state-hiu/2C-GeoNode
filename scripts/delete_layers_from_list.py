import django
django.setup()
from geonode.layers.models import Layer
import csv
import sys

with open(sys.argv[1], 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='"')
    for row in reader:
        try:
            layer = Layer.objects.get(name=row[0].lower())
            layer.delete()
            print "[SUCESS] Layer [%s] deleted" % (layer.name)
        except:
            print "[ERROR] Layer [%s] couldn't be deleted" % (layer.name)
