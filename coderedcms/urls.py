from django.urls import path, re_path
from django.contrib.auth.views import LoginView
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.core.urls import serve_pattern, WAGTAIL_FRONTEND_LOGIN_TEMPLATE
from wagtail.core import views as wagtail_views
from wagtailcache.cache import cache_page

from coderedcms.settings import cr_settings
from coderedcms.views import (
    event_generate_ical_for_calendar,
    event_generate_recurring_ical_for_event,
    event_generate_single_ical_for_event,
    event_get_calendar_events,
    robots, 
    serve_protected_file
)


urlpatterns = [
    # CodeRed custom URLs
    re_path(r'^sitemap\.xml$', cache_page(sitemap), name='codered_sitemap'),
    re_path(r'^robots\.txt$', cache_page(robots), name='codered_robots'),
    re_path(r'^{0}(?P<path>.*)$'.format(cr_settings['PROTECTED_MEDIA_URL'].lstrip('/')), serve_protected_file, name="serve_protected_file"),

    # Direct copy of wagtail.core.urls
    re_path(
        r'^_util/authenticate_with_password/(\d+)/(\d+)/$',
        wagtail_views.authenticate_with_password,
        name='wagtailcore_authenticate_with_password'
    ),
    path('_util/login/', LoginView.as_view(template_name=WAGTAIL_FRONTEND_LOGIN_TEMPLATE), name='wagtailcore_login'),

    #ICAL URLS
    path('ical/generate/single/', event_generate_single_ical_for_event, name='event_generate_single_ical'),
    path('ical/generate/recurring/', event_generate_recurring_ical_for_event, name='event_generate_recurring_ical'),
    path('ical/generate/calendar/', event_generate_ical_for_calendar, name='event_generate_ical_for_calendar'),

    #Calendar URLS
    path('ajax/calendar/events/', event_get_calendar_events, name='event_get_calendar_events'),

    # Wrap the serve function with coderedcms cache
    re_path(serve_pattern, cache_page(wagtail_views.serve), name='wagtail_serve'),

]
