import pytest
import unittest

from django.urls import reverse
from django.test import Client
from django.test.utils import override_settings
from django.conf import settings

from wagtail.core.models import Site
from wagtail.images.tests.utils import Image, get_test_image_file

from coderedcms.models import LayoutSettings
from coderedcms.tests.testapp.models import EventPage, EventIndexPage, WebPage


@pytest.mark.django_db
class URLTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    @override_settings(DEBUG=False)
    def test_404(self):
        response = self.client.get("/testing/404/page/", follow=True)

        self.assertEqual(response.status_code, 404)

    def test_sitemap(self):
        response = self.client.get("/sitemap.xml", follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/xml')

    def test_robots(self):
        response = self.client.get("/robots.txt", follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'text/plain')

    def test_search(self):
        response = self.client.get(reverse('codered_search'), {'s': 'Test Search Query'}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.context['results'], None)

    def test_generate_single_event(self):
        event_page = EventPage.objects.create(path='/event/', depth=1, title='Event', slug='event')

        response = self.client.post("/ical/generate/single/", {'event_pk': event_page.pk, 'datetime_start': '2019-01-01T9:00:00Z', 'datetime_end': '2019-01-01T10:30:00Z'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Filename'], "{0}.ics".format(event_page.slug))
        self.assertEqual(response['Content-Disposition'], 'attachment; filename={0}.ics'.format(event_page.slug))

    def test_generate_recurring_event(self):
        event_page = EventPage.objects.create(path='/event/', depth=1, title='Event', slug='event')

        response = self.client.post("/ical/generate/recurring/", {'event_pk': event_page.pk}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Filename'], "{0}.ics".format(event_page.slug))
        self.assertEqual(response['Content-Disposition'], 'attachment; filename={0}.ics'.format(event_page.slug))

    def test_generate_calendar(self):
        page = WebPage.objects.create(path='/page/', depth=1, title='Page', slug='page')

        response = self.client.post("/ical/generate/calendar/", {'page_id': page.pk}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Filename'], 'calendar.ics')
        self.assertEqual(response['Content-Disposition'], 'attachment; filename=calendar.ics')

    def test_ajax_calendar(self):
        page = EventIndexPage.objects.create(path='/page/', depth=1, title='Page', slug='page')

        response = self.client.post("/ajax/calendar/events/?pid=" + str(page.pk), follow=True, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.status_code, 200)


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
