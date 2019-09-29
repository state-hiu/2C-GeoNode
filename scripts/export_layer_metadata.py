import django
django.setup()

from geonode.layers.models import Layer
from geonode.base.models import ResourceBase
import unicodecsv as csv
import sys

all_layers = Layer.objects.all()

csv_file = open("layers_list.csv", "wb")
writer = csv.writer(csv_file, delimiter=';')

for layer in all_layers:
	name = layer.name
	title = layer.title
	abstract = layer.abstract
	category = layer.category
	keywords_list = [k.name for k in layer.keywords.all()] if layer.keywords else []
	keywords = ','.join(keywords_list)
	purpose = layer.purpose
	date = ""
	data_quality = layer.data_quality_statement
	lineage = layer.lineage
	dataprovidertype = layer.dataprovidertype
	dataprovider_name = layer.dataprovider_name
	dataprovider_contact = layer.dataprovider_contact
	dataprovider_url = layer.dataprovider_url
	supplemental_information = layer.supplemental_information
	constraints_other = layer.constraints_other
	city = layer.city
	language = layer.language

	# stype = layer.display_type
	# if (len(layer.link_set.filter(name='JPEG'))>0):
	# 	wms_jpeg = layer.link_set.filter(name='JPEG')[0].url
	# else:
	# 	wms_jpeg = ""
	data = [name, title, abstract, category, keywords, purpose, date, data_quality, lineage, dataprovidertype, dataprovider_name, dataprovider_contact, dataprovider_url, supplemental_information, constraints_other, city, language]
	writer.writerow(data)

csv_file.close()
