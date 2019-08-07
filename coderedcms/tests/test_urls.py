import pytest
import unittest
from django.test import Client
from coderedcms.models import LayoutSettings
from wagtail.core.models import Site
from wagtail.images.tests.utils import Image, get_test_image_file


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
