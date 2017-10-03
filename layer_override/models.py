from django.db import models
from geonode.layers.models import Layer
from monkeypatch.utils import decorator as monkey_patch


@monkey_patch(Layer)
class Layerextension(object):
    dataprovidertype = models.CharField(max_length=128,null=True)     



