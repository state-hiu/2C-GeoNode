from geoserver.catalog import Catalog

cat = Catalog('http://localhost:8080/geoserver/rest')
ds = cat.create_datastore('state_2c_geonode','geonode')
ds.connection_parameters.update(host='localhost', port='5432', database='state_2c_geonode', user='state_2c_geonode', passwd='state_2c_geonode', dbtype='postgis', schema='public')
try:
    cat.save(ds)
except Exception as e:
    print e

