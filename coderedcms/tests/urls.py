from django.conf.urls import include, url
from django.http import HttpResponse

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.api.v2.endpoints import PagesAPIEndpoint
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.contrib.sitemaps import views as sitemaps_views
from wagtail.contrib.sitemaps import Sitemap
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.documents.api.v2.endpoints import DocumentsAPIEndpoint
from wagtail.images import urls as wagtailimages_urls
from wagtail.images.api.v2.endpoints import ImagesAPIEndpoint

api_router = WagtailAPIRouter('wagtailapi_v2')
api_router.register_endpoint('pages', PagesAPIEndpoint)
api_router.register_endpoint('images', ImagesAPIEndpoint)
api_router.register_endpoint('documents', DocumentsAPIEndpoint)


urlpatterns = [
    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'^images/', include(wagtailimages_urls)),

    url(r'^api/v2beta/', api_router.urls),

    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's serving mechanism
    url(r'', include(wagtail_urls)),
]