from django.urls import path
from coderedcms.views import search

urlpatterns = [
    path("", search, name="crx_search"),
]
