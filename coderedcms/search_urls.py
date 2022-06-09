from django.urls import path
from coderedcms.views import search

urlpatterns = [
    path('', search, name='codered_search'),
]
