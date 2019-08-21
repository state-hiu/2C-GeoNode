import django
django.setup()

from django.core.management.base import BaseCommand
from guardian.shortcuts import get_objects_for_user
from geonode.people.models import Profile
from geonode.layers.models import Layer
from geonode.security.utils import set_geofence_all
from geonode.security.utils import get_users_with_perms
import csv
import sys

profiles = Profile.objects.filter(is_superuser=False)
authorized = list(get_objects_for_user(profiles[0], 'base.view_resourcebase').values('id'))
all_layers = Layer.objects.all()
unprotected_layers = Layer.objects.filter(id__in=[d['id'] for d in authorized])
protected_layers = Layer.objects.all().exclude(id__in=[d['id'] for d in authorized])

with open(sys.argv[1], 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='"')
    for row in reader:
        try:
            layer = Layer.objects.get(name=row[0].lower())
            set_geofence_all(layer)
            layer.set_default_permissions()
            perm_spec = {"users": {}, "groups": {}}
            perm_spec["users"]["admin"] = ['view_resourcebase','change_resourcebase_permissions','download_resourcebase','publish_resourcebase','change_resourcebase_metadata']
            perm_spec["users"][str(layer.owner)] = ['view_resourcebase','change_resourcebase_permissions','download_resourcebase','publish_resourcebase','change_resourcebase_metadata']
            perm_spec["users"]["AnonymousUser"] = ['view_resourcebase','download_resourcebase']
            #perm_spec = {"users": {"admin": ['view_resourcebase','change_resourcebase_permissions','download_resourcebase','publish_resourcebase','change_resourcebase_metadata'], "AnonymousUser": ['view_resourcebase','download_resourcebase']}, "groups": {}}
            layer.set_permissions(perm_spec)
            print "[SUCESS] Layer [%s] permissions were updated" % (layer.name)
        except:
            print "[ERROR] Layer [%s] couldn't be updated" % (layer.name)
