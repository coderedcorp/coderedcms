from django.conf.urls import include, url
from wagtailimportexport import urls as wagtailimportexport_urls
from wagtail.admin import urls as wagtailadmin_urls
from coderedcms.views import clear_cache, import_pages_from_csv_file


urlpatterns = [
    url(r'^codered/clearcache$', clear_cache, name="clear_cache"),
    url(r'^codered/import-export/import_from_csv/$', import_pages_from_csv_file, name="import_from_csv"),
    url(r'', include(wagtailadmin_urls)),
    url(r'', include(wagtailimportexport_urls)),
]
