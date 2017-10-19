from collections import Counter
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from geonode.api.resourcebase_api import CommonModelApi, CommonMetaApi
from geonode.layers.models import Layer
from geonode.maps.models import Map
from geonode.documents.models import Document
from geonode.base.models import ResourceBase
from django.conf import settings
from geonode.api.resourcebase_api import ResourceBaseResource, FeaturedResourceBaseResource,DocumentResource, MapResource
from collections import Counter

class FullTextModelApi(CommonModelApi):
   VALUES = [
        # fields in the db
        'id',
        'uuid',
        'title',
        'date',
        'abstract',
        'csw_wkt_geometry',
        'csw_type',
        'owner__username',
        'share_count',
        'popular_count',
        'srid',
        'category__gn_description',
        'supplemental_information',
        'thumbnail_url',
        'detail_url',
        'rating',
	'keywords__name',
    ]
   def format_objects(self, objects):
        """
        Format the objects for output in a response.
        """
	return objects.values(*self.VALUES)
   def get_list(self, request, **kwargs):
        """
        Returns a serialized list of resources.

        Calls ``obj_get_list`` to provide the data, then handles that result
        set and serializes it.

        Should return a HttpResponse (200 OK).
        """
        # TODO: Uncached for now. Invalidation that works for everyone may be
        # impossible.
 	query_sql="SELECT id, title, ts_rank_cd(to_tsvector(csw_anytext), query) as rank from base_resourcebase, to_tsquery('{0}') query where to_tsvector(csw_anytext) @@ query order by rank desc;"
	if 'q' in request.GET:
		search_query=request.GET['q']
		search_query=search_query.replace(' ','&')
		query_sql=query_sql.format(search_query)
		#if  layers are being searched
          	if request.path=='/api/layers/':
            		id_objects=[item.id for item in ResourceBase.objects.raw(query_sql) if hasattr(item, 'layer')]
            		base_bundle = self.build_bundle(request=request)
			queryset = self.obj_get_list(
                        	    bundle=base_bundle,
                                    **self.remove_api_resource_names(kwargs))
			objects = queryset.filter(pk__in=id_objects)
			if 'dataprovider_type__in' in request.GET:
				params=dict(request.GET)
                        	objects = objects.filter(dataprovidertype__in=params['dataprovider_type__in'])
			sorted_objects=objects #objects are sorted by matching ranking
	else:
            	base_bundle = self.build_bundle(request=request)
           	objects = self.obj_get_list(
               		bundle=base_bundle,
               		**self.remove_api_resource_names(kwargs))
		if 'dataprovider_type__in' in request.GET:
			params=dict(request.GET)
			objects = objects.filter(dataprovidertype__in=params['dataprovider_type__in'])
            	sorted_objects = self.apply_sorting(objects, options=request.GET)

        paginator = self._meta.paginator_class(
            request.GET,
            sorted_objects,
            resource_uri=self.get_resource_uri(),
            limit=self._meta.limit,
            max_limit=self._meta.max_limit,
            collection_name=self._meta.collection_name)
        to_be_serialized = paginator.page()
        to_be_serialized = self.alter_list_data_to_serialize(
            request,
            to_be_serialized)

	keywords = list_key=[layer.keyword_list() for layer in objects]
	flat_list = [item for sublist in keywords for item in sublist]
	to_be_serialized['facet_keywords']=dict(Counter(flat_list))
        return self.create_response(request, to_be_serialized, response_objects=objects)


class LayerResource(FullTextModelApi):

    """Layer API"""

    class Meta(CommonMetaApi):
        queryset = Layer.objects.distinct().order_by('-date')
        if settings.RESOURCE_PUBLISHING:
            queryset = queryset.filter(is_published=True)
        resource_name = 'layers'
        excludes = ['csw_anytext', 'metadata_xml']

