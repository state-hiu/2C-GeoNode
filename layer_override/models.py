from django.db import models
from geonode.layers.models import Layer
from monkeypatch.utils import decorator as monkey_patch


@monkey_patch(Layer)
class Layerextension(object):
    lineage = models.TextField(blank=True,null=True)
    city = models.CharField(max_length=128,blank=True,null=True)
    dataprovider_name = models.CharField(max_length=128,blank=True,null=True)
    dataprovider_url = models.CharField(max_length=255, null=True, blank=True)
    dataprovider_contact = models.CharField(max_length=128,blank=True,null=True) 
    dataprovidertype = models.CharField(max_length=128,null=True)
