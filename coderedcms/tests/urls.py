from django.urls import include, path, re_path
from django.contrib import admin
from wagtail.documents import urls as wagtaildocs_urls
from coderedcms import admin_urls as crx_admin_urls
from coderedcms import search_urls as crx_search_urls
from coderedcms import urls as crx_urls

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(crx_admin_urls)),
    path("docs/", include(wagtaildocs_urls)),
    path("search/", include(crx_search_urls)),
    re_path(r"", include(crx_urls)),
]
