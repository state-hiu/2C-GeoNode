cities = [
    { "name": "Cusco, Peru", "keyword": "Cusco", "image": "/static/img/Cusco3.jpg"},
    { "name": "Denpasar, Indonesia", "keyword": "Denpasar", "image": ""},
    { "keyword": "Douala", "name": "Douala, Cameroon", "image": "/static/img/douala_web4.jpg" },
    { "keyword": "Esmeraldas", "name": "Esmeraldas, Ecuador", "image": "/static/img/esmeraldas_web.jpg" },
    { "keyword": "Kharkiv", "name": "Kharkiv, Ukraine", "image": "/static/img/Kharkiv4.jpg" },
    { "keyword": "Medellin", "name": "Medellin, Colombia", "image": "/static/img/medellin4.jpg" },
    { "keyword": "Merkelle", "name": "Mekelle, Ethiopia", "image": "/static/img/mekelle3.jpg" },
    { "keyword": "Pokhara", "name": "Pokhara, Nepal", "image": "/static/img/pokhara3.jpg" },
    { "keyword": "Port Harcourt", "name": "Port Harcourt, Nigeria", "image": "/static/img/portharcourt_web.jpg" },
    { "keyword": "Santiago", "name": "Santiago, Dominican Republic", "image": "/static/img/santiago_web.jpg" }
]


from django import template

register = template.Library()

@register.assignment_tag
def get_cities():
    return cities
