from django.urls import re_path

from coderedcms.views import search
from coderedcms.utils import cache_page

urlpatterns = [
    re_path(r'', cache_page(search), name='codered_search'),
]
