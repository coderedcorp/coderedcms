from django.conf.urls import include, url
from wagtail.admin import urls as wagtailadmin_urls
from coderedcms.core.views import clear_cache
from coderedcms.core.settings import cr_settings


urlpatterns = [
    url(r'^codered/clearcache$', clear_cache, name="clear_cache"),
    url(r'', include(wagtailadmin_urls)),
]