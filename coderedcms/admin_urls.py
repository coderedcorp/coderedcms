from django.urls import include, path, re_path
from wagtail.admin import urls as wagtailadmin_urls
from coderedcms.views import import_index, import_pages_from_csv_file


urlpatterns = [
    path('codered/import-export/',
         import_index, name="import_index"),
    path('codered/import-export/import_from_csv/',
         import_pages_from_csv_file, name="import_from_csv"),
    re_path(r'', include(wagtailadmin_urls)),
]
