from unittest.mock import patch

from django.test import Client
from django.test import override_settings
from wagtail.models import Site
from wagtail.test.utils import WagtailPageTests

from coderedcms.models.wagtailsettings_models import AnalyticsSettings
from coderedcms.models.wagtailsettings_models import maybe_register_setting
from coderedcms.tests.testapp.models import WebPage


class AnalyticsSettingsTestCase(WagtailPageTests):
    """
    Test that the relevant analytics settings appear in the homepage HTML.
    """

    model = WebPage

    def setUp(self):
        # HTTP client.
        self.client = Client()

        # Use home page and default site.
        self.site = Site.objects.filter(is_default_site=True)[0]
        self.homepage = WebPage.objects.get(url_path="/home/")

        # Populate settings.
        self.settings = AnalyticsSettings.for_site(self.site)
        self.settings.ga_g_tracking_id = "G-123"
        self.settings.head_scripts = "<script>evil_tracker</script>"
        self.settings.body_scripts = "<script>annoying_tracker</script>"
        self.settings.save()

    def test_get(self):
        """
        Tests to make sure the page serves a 200 from a GET request.
        """
        response = self.client.get(self.homepage.url, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_ga_g_tracking_id(self):
        """
        Make sure the ga_g_tracking_id is present.
        """
        response = self.client.get(self.homepage.url, follow=True)
        self.assertIn(self.settings.ga_g_tracking_id, str(response.content), 1)

    def test_head_scripts(self):
        """
        Make sure the head_scripts is present.
        """
        response = self.client.get(self.homepage.url, follow=True)
        self.assertInHTML(self.settings.head_scripts, str(response.content), 1)

    def test_body_scripts(self):
        """
        Make sure the body_scripts is present.
        """
        response = self.client.get(self.homepage.url, follow=True)
        self.assertInHTML(self.settings.body_scripts, str(response.content), 1)


class MaybeRegisterSettingTestCase(WagtailPageTests):
    """Testing the maybe_register_setting decorator.

    These tests use a dummy settings object to test the two paths
    through the decorator which determine whether or not register_settings
    is called."""

    def setUp(self):
        super().setUp()
        self.dummy_settings = object()

    @override_settings(CRX_DISABLE_LAYOUT=False)
    @patch("coderedcms.models.wagtailsettings_models.register_setting")
    def test_decorator_enabled(self, mock_register_setting):
        """Test that the decorator calls register_setting
        when override setting is False."""
        maybe_register_setting(False, icon="foobar")(self.dummy_settings)
        mock_register_setting.assert_called_once_with(
            self.dummy_settings, icon="foobar"
        )

    @override_settings(CRX_DISABLE_SITE_SETTINGS=True)
    @patch("coderedcms.models.wagtailsettings_models.register_setting")
    def test_decorator_disabled(self, mock_register_setting):
        """Test that the decorator does not call register_setting
        when override setting is False."""
        maybe_register_setting(True, icon="foobar")(self.dummy_settings)
        mock_register_setting.assert_not_called()
