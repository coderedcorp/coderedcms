from django.urls import path
from wagtailcrx.views import search

urlpatterns = [
    path('', search, name='codered_search'),
]
