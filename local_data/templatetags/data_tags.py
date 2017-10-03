from django import template
from django.conf import settings

register = template.Library()
data_provider_type = [
			{'id':'global_downld_data', 'value':'Global Downloaded Data'},
			{'id':'local_downld_data', 'value':'Local Downloaded Data'},
		 	{'id':'local_auth_data', 'value':'Local Authoritative Data'},
			{'id':'local_workshop_data', 'value':'Local Workshop Data'}
		     ]

@register.assignment_tag
def get_data_provide_types():
    return data_provider_type

@register.assignment_tag
def get_cities():
    return settings.CITIES
