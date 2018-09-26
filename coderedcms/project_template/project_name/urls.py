from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from wagtail.documents import urls as wagtaildocs_urls
from coderedcms.core import admin_urls as coderedadmin_urls
from coderedcms.search import urls as coderedsearch_urls
from coderedcms.core import urls as codered_urls

urlpatterns = [
    # Admin
    url(r'^django-admin/', admin.site.urls),
    url(r'^admin/', include(coderedadmin_urls)),

    # Documents
    url(r'^docs/', include(wagtaildocs_urls)),

    # Search
    url(r'^search/', include(coderedsearch_urls)),

    # For anything not caught by a more specific rule above, hand over to
    # the page serving mechanism. This should be the last pattern in
    # the list:
    url(r'', include(codered_urls)),

    # Alternatively, if you want CMS pages to be served from a subpath
    # of your site, rather than the site root:
    #    url(r'^pages/', include(codered_urls)),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
