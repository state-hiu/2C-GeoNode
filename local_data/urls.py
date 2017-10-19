from tastypie.api import Api

from geonode.api.api import TagResource, TopicCategoryResource, ProfileResource, \
    GroupResource, RegionResource, OwnersResource, ThesaurusKeywordResource 
from .resourcebase_api import LayerResource, DocumentResource, \
    ResourceBaseResource, FeaturedResourceBaseResource,MapResource

api = Api(api_name='api')
api.register(MapResource())
api.register(LayerResource())
api.register(DocumentResource())
api.register(ProfileResource())
api.register(ResourceBaseResource())
api.register(TagResource())
api.register(RegionResource())
api.register(TopicCategoryResource())
api.register(GroupResource())
api.register(FeaturedResourceBaseResource())
api.register(OwnersResource())
api.register(ThesaurusKeywordResource())
