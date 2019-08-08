import django
django.setup()
from geonode.layers.models import Layer
from geonode.base.models import Region
from geonode.base.models import ResourceBase
from geonode.base.models import HierarchicalKeyword
from geonode.base.models import SpatialRepresentationType
from geonode.base.models import TopicCategory
from geonode.people.models import Profile
import csv
import pycountry
import sys

with open(sys.argv[1], 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='"')
    for row in reader:
        try:
            layer = Layer.objects.get(name=row[0].lower())
            layer.title = row[1]
            layer.abstract = row[2]
            try:
                topic_test = TopicCategory.objects.get(description=row[3].strip())
            except:
                topic = TopicCategory(identifier=row[3].lower(), description=row[3].strip(), gn_description=row[3].strip())
                topic.save()
            layer.category = TopicCategory.objects.get(description=row[3].strip())

            kwds = row[4].split(',')
            for k in kwds:
                ks = k.strip()
                try:
                    key_test = HierarchicalKeyword.objects.get(name=ks)
                except:
                    new_key = HierarchicalKeyword.add_root(name=ks)
                    new_key.save()
                keyw = HierarchicalKeyword.objects.get(name=ks)
                layer.keywords.add(keyw)

            layer.purpose = row[5]
            #layer.date = row[6] #Disabled by default
            layer.data_quality_statement = row[7]
            layer.lineage = row[8]
            layer.dataprovidertype = row[9].strip()
            layer.dataprovider_name = row[10]
            layer.dataprovider_contact = row[11]
            layer.dataprovider_url = row[12]
            layer.supplemental_information = row[13]
            layer.constraints_other = row[14]
            try:
                city_name = layer.title.split(':')[0].strip().replace(' ','_')
                layer.city = city_name
            except:
                layer.city = None
            
            try:
                tmp_lang = row[15].split(', ')[0] #FIXME
                lang = pycountry.languages.get(name=tmp_lang)
                layer.language = str(lang.alpha_3)
            except:
                layer.language = "eng"
            
            #if (row[16] != "Unknown"):
            #    layer.maintenance_frequency = row[16]
            #layer.owner = Profile.objects.get(username=row[18])

            layer.save()

            #resource = layer.get_self_resource()

            print "%s : Metadata updated!" % layer.title
        except Exception, e:
            print "%s : Failed to update" % row[1].lower()
            print "Exception: %s" % str(e)
