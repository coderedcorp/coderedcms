from django.urls import include
from django.urls import path
from django.urls import re_path
from wagtail import urls as wagtailcore_urls
from wagtail.contrib.sitemaps.views import sitemap

from coderedcms.settings import crx_settings
from coderedcms.views import event_generate_ical_for_calendar
from coderedcms.views import event_generate_recurring_ical_for_event
from coderedcms.views import event_generate_single_ical_for_event
from coderedcms.views import event_get_calendar_events
from coderedcms.views import favicon
from coderedcms.views import robots
from coderedcms.views import serve_protected_file


urlpatterns = [
    # CodeRed custom URLs
    path(r"favicon.ico", favicon, name="crx_favicon"),
    path(r"robots.txt", robots, name="crx_robots"),
    path(r"sitemap.xml", sitemap, name="crx_sitemap"),
    re_path(
        r"^{0}(?P<path>.*)$".format(
            crx_settings.CRX_PROTECTED_MEDIA_URL.lstrip("/")
        ),
        serve_protected_file,
        name="serve_protected_file",
    ),
    # Event/Calendar URLs
    path(
        "ical/generate/single/",
        event_generate_single_ical_for_event,
        name="event_generate_single_ical",
    ),
    path(
        "ical/generate/recurring/",
        event_generate_recurring_ical_for_event,
        name="event_generate_recurring_ical",
    ),
    path(
        "ical/generate/calendar/",
        event_generate_ical_for_calendar,
        name="event_generate_ical_for_calendar",
    ),
    path(
        "ajax/calendar/events/",
        event_get_calendar_events,
        name="event_get_calendar_events",
    ),
    # Wagtail
    path("", include(wagtailcore_urls)),
]
