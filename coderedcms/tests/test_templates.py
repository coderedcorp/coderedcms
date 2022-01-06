from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase

from coderedcms.templatetags.coderedcms_tags import cr_settings


@pytest.mark.django_db
class TestSiteBanner(TestCase):

    @patch.dict(cr_settings, {"BANNER": "Test"})
    def test_with_banner(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertInHTML(
            '<div class="codered-banner" style="background-color:#f00; color:#fff; width:100%; padding:4px;">'
            "Test</div>",
            response.content.decode("utf-8")
        )

    def test_without_banner(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("codered-banner", response.content.decode("utf-8"))


@pytest.mark.django_db
class TestWagtailAdminBanner(TestCase):
    def setUp(self):
        admin = get_user_model().objects.create_superuser("admin", email="admin@example.com", password="admin")
        self.client.force_login(admin)

    def tearDown(self):
        self.client.logout()

    @patch.dict(cr_settings, {"BANNER": "Test"})
    def test_with_banner(self):
        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 200)
        self.assertInHTML(
            '<div class="codered-banner" style="background-color:#f00; color:#fff; width:100%; padding:4px;">'
            "Test</div>",
            response.content.decode("utf-8")
        )

    def test_without_banner(self):
        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("codered-banner", response.content.decode("utf-8"))
