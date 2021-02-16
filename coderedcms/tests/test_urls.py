import pytest
import unittest

from ast import literal_eval

from django.urls import reverse
from django.test import Client
from django.test.utils import override_settings

from wagtail.core.models import Site, Page
from wagtail.images.tests.utils import Image, get_test_image_file

from coderedcms.models import LayoutSettings
from coderedcms.tests.testapp.models import EventPage, EventIndexPage, EventOccurrence


@pytest.mark.django_db
class TestSiteURLs(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    @override_settings(DEBUG=False)
    def test_404(self):
        response = self.client.get("/testing/404/page/", follow=True)

        self.assertEqual(response.status_code, 404)

    def test_sitemap(self):
        response = self.client.get("/sitemap.xml")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/xml')

    def test_robots(self):
        response = self.client.get("/robots.txt")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'text/plain')

    def test_search(self):
        response = self.client.get(reverse(
            'codered_search'),
            {'s': 'Test Search Query'},
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.context['results'], None)

        response = self.client.get(reverse(
            'codered_search'),
            {
                's': 'keyword',
                't': 't',
            },
            follow=False
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['results'], None)


@pytest.mark.django_db
class TestEventURLs(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.root_page = Page.get_root_nodes()[0]

    def test_generate_single_event(self):
        event_page = EventPage(
            path='/single-event/',
            depth=1,
            title='Single Event',
            slug='single-event'
        )
        self.root_page.add_child(instance=event_page)
        occurrence = EventOccurrence(
            event=event_page,
            start='2019-01-01T10:00:00+0000',
            end='2019-01-01T11:00:00+0000'
        )
        occurrence.save()

        response = self.client.post(
            "/ical/generate/single/",
            {
                'event_pk': event_page.pk,
                'datetime_start': EventOccurrence.objects.get(
                    event=event_page
                ).start.strftime("%Y-%m-%d %H:%M:%S%z").replace(' ', 'T'),
                'datetime_end': EventOccurrence.objects.get(
                    event=event_page
                ).end.strftime("%Y-%m-%d %H:%M:%S%z").replace(' ', 'T'),
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Filename'], "{0}.ics".format(event_page.slug))
        self.assertEqual(
            response['Content-Disposition'],
            'attachment; filename={0}.ics'.format(event_page.slug)
        )
        self.assertEqual(response['content-type'], 'text/calendar')

        # Get datetimes from response and compare them to datetimes on page
        # startswith() is used because older versions of Python
        # use different datetime formatting, specifically for timezones
        split_content = str(response._container[0]).split('VALUE=DATE-TIME:')
        start = split_content[1].split('\\')[0]
        end = split_content[2].split('\\')[0]
        self.assertTrue(
            start.startswith(
                EventOccurrence.objects.get(event=event_page).start.strftime("%Y%m%dT%H%M%S")
            )
        )
        self.assertTrue(
            end.startswith(
                EventOccurrence.objects.get(event=event_page).end.strftime("%Y%m%dT%H%M%S")
            )
        )

    def test_generate_recurring_event(self):
        event_page = EventPage(
            path='/recurring-event/',
            depth=1,
            title='Recurring Event',
            slug='recurring-event'
        )
        self.root_page.add_child(instance=event_page)
        occurrence = EventOccurrence(
            event=event_page,
            start='2019-01-01T10:00:00+0000',
            end='2019-01-01T11:00:00+0000'
        )
        occurrence.save()

        response = self.client.post(
            "/ical/generate/recurring/",
            {'event_pk': event_page.pk},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Filename'], "{0}.ics".format(event_page.slug))
        self.assertEqual(
            response['Content-Disposition'],
            'attachment; filename={0}.ics'.format(event_page.slug)
        )
        self.assertEqual(response['content-type'], 'text/calendar')

        # Get datetimes from response and compare them to datetimes on page
        # startswith() is used because older versions of Python
        # use different datetime formatting, specifically for timezones
        split_content = str(response._container[0]).split('VALUE=DATE-TIME:')
        start = split_content[1].split('\\')[0]
        end = split_content[2].split('\\')[0]
        self.assertTrue(
            start.startswith(
                EventOccurrence.objects.get(event=event_page).start.strftime("%Y%m%dT%H%M%S")
            )
        )
        self.assertTrue(
            end.startswith(
                EventOccurrence.objects.get(event=event_page).end.strftime("%Y%m%dT%H%M%S")
            )
        )

    def test_generate_calendar(self):
        calendar_page = EventIndexPage(
            path='/event-index-page/',
            depth=1,
            title='Event Index Page',
            slug='event-index-page'
        )
        self.root_page.add_child(instance=calendar_page)

        event_page = EventPage(
            path='/eventpage/1/',
            depth=2,
            title='Event Page 1',
            slug='eventpage1'
        )
        calendar_page.add_child(instance=event_page)
        occurrence = EventOccurrence(
            event=event_page,
            start='2019-01-01T10:00:00+0000',
            end='2019-01-01T11:00:00+0000'
        )
        occurrence.save()

        response = self.client.post(
            "/ical/generate/calendar/",
            {'page_id': calendar_page.pk},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Filename'], 'calendar.ics')
        self.assertEqual(response['Content-Disposition'], 'attachment; filename=calendar.ics')
        self.assertEqual(response['content-type'], 'text/calendar')

        # Get datetimes from response and compare them to datetimes on page
        # startswith() is used because older versions of Python
        # use different datetime formatting, specifically for timezones
        split_content = str(response._container[0]).split('VALUE=DATE-TIME:')
        start = split_content[1].split('\\')[0]
        end = split_content[2].split('\\')[0]
        self.assertTrue(
            start.startswith(
                EventOccurrence.objects.get(event=event_page).start.strftime("%Y%m%dT%H%M%S")
            )
        )
        self.assertTrue(
            end.startswith(
                EventOccurrence.objects.get(event=event_page).end.strftime("%Y%m%dT%H%M%S")
            )
        )

    def test_ajax_calendar(self):
        calendar_page = EventIndexPage(
            path='/event-index-page/',
            depth=1,
            title='Event Index Page',
            slug='event-index-page'
        )
        self.root_page.add_child(instance=calendar_page)

        event_page = EventPage(
            path='/eventpage/1/',
            depth=2,
            title='Event Page 1',
            slug='eventpage1'
        )
        calendar_page.add_child(instance=event_page)
        occurrence_one = EventOccurrence(
            event=event_page,
            start='2019-01-01T10:00:00+0000',
            end='2019-01-01T11:00:00+0000'
        )
        occurrence_one.save()

        response = self.client.post(
            "/ajax/calendar/events/?pid=" + str(calendar_page.pk),
            follow=True,
            **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
        )
        self.assertEqual(response.status_code, 200)

        # Get datetimes from response and compare them to datetimes on page
        start = literal_eval(response._container[0].decode()[1:-1])['start']
        end = literal_eval(response._container[0].decode()[1:-1])['end']
        self.assertEqual(
            start,
            EventOccurrence.objects.get(event=event_page).start.strftime("%Y-%m-%dT%H:%M:%S")
        )
        self.assertEqual(
            end,
            EventOccurrence.objects.get(event=event_page).end.strftime("%Y-%m-%dT%H:%M:%S")
        )


@pytest.mark.django_db
class TestFavicon(unittest.TestCase):
    def test_404(self):
        client = Client()
        # Get the default site
        site = Site.objects.filter(is_default_site=True)[0]
        # Ensure the favicon is blank
        layout = LayoutSettings.for_site(site)
        layout.favicon = None
        layout.save()
        # Expect a 404
        response = client.get("/favicon.ico")
        self.assertEqual(response.status_code, 404)

    def test_301(self):
        client = Client()
        # Get the default site
        site = Site.objects.filter(is_default_site=True)[0]
        # Set a dummy favicon
        layout = LayoutSettings.for_site(site)
        img = Image.objects.create(
            title="Test image",
            file=get_test_image_file(),
        )
        layout.favicon = img
        layout.save()
        # Expect a 301 redirect
        response = client.get("/favicon.ico")
        self.assertEqual(response.status_code, 301)
