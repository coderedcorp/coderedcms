from django.conf.urls import url

from coderedcms.views import search
from coderedcms.utils import cache_page

urlpatterns = [
    url(r'', cache_page(search), name='codered_search'),
]
