from django.urls import re_path
from wagtailcache.cache import cache_page

from coderedcms.views import search

urlpatterns = [
    re_path(r'', cache_page(search), name='codered_search'),
]
