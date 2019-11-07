from django.urls import include, path, re_path
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.core import urls as wagtailcore_urls
from coderedcms.settings import cr_settings
from coderedcms.views import (
    event_generate_ical_for_calendar,
    event_generate_recurring_ical_for_event,
    event_generate_single_ical_for_event,
    event_get_calendar_events,
    favicon,
    robots,
    serve_protected_file
)


urlpatterns = [
    # CodeRed custom URLs
    re_path(r'^favicon\.ico$', favicon, name='codered_favicon'),
    re_path(r'^robots\.txt$', robots, name='codered_robots'),
    re_path(r'^sitemap\.xml$', sitemap, name='codered_sitemap'),
    re_path(r'^{0}(?P<path>.*)$'.format(
        cr_settings['PROTECTED_MEDIA_URL'].lstrip('/')),
        serve_protected_file,
        name="serve_protected_file"
    ),

    # Event/Calendar URLs
    path('ical/generate/single/', event_generate_single_ical_for_event,
         name='event_generate_single_ical'),
    path('ical/generate/recurring/', event_generate_recurring_ical_for_event,
         name='event_generate_recurring_ical'),
    path('ical/generate/calendar/', event_generate_ical_for_calendar,
         name='event_generate_ical_for_calendar'),
    path('ajax/calendar/events/', event_get_calendar_events, name='event_get_calendar_events'),

    # Wagtail
    re_path(r'', include(wagtailcore_urls)),
]
