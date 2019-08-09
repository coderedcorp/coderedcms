from django.test import Client, TestCase
from django.urls import reverse
import unittest
import pytest

from django.test.utils import override_settings
from django.conf import settings

from coderedcms.tests.testapp.models import EventPage, EventIndexPage, WebPage


@pytest.mark.django_db
class URLTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    # Switch DEBUG to false and then back?
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
