from django.conf.urls import url

from coderedcms.search.views import search
from coderedcms.core.utils import cache_page

urlpatterns = [
    url(r'', cache_page(search), name='codered_search'),
]
