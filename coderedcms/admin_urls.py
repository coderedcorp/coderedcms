from django.conf.urls import include, url
from wagtail.admin import urls as wagtailadmin_urls
from coderedcms.views import clear_cache


urlpatterns = [
    url(r'^codered/clearcache$', clear_cache, name="clear_cache"),
    url(r'', include(wagtailadmin_urls)),
]
