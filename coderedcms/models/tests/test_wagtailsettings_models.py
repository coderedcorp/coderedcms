from unittest.mock import patch

from django.test import Client, override_settings
from wagtail.test.utils import WagtailPageTests
from wagtail.models import Site

from coderedcms.tests.testapp.models import WebPage
from coderedcms.models.wagtailsettings_models import (
    AnalyticsSettings,
    LayoutSettings,
    maybe_register_setting,
    SettingsCheckMixin,
)


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


class SettingsCheckTestCase(WagtailPageTests):

    def setUp(self):
        super().setUp()
        self.site = Site.objects.get(is_default_site=True)
        self.layout_settings = LayoutSettings.for_site(self.site)
        self.analytics_settings = AnalyticsSettings.for_site(self.site)

    def test_layoutsettings_default(self):
        self.assertTrue(self.layout_settings.enabled())

    @override_settings(CRX_ENABLE_LAYOUT_SETTINGS=True)
    def test_layoutsettings_enabled(self):

        self.assertTrue(self.layout_settings.enabled())

    @override_settings(CRX_ENABLE_LAYOUT_SETTINGS=False)
    def test_layoutsettings_disabled(self):

        self.assertFalse(self.layout_settings.enabled())

    def test_analyticssettings_default(self):

        self.assertTrue(self.analytics_settings.enabled())

    @override_settings(CRX_ENABLE_ANALYTICS_SETTINGS=True)
    def test_analyticssettings_enabled(self):

        self.assertTrue(self.analytics_settings.enabled())

    @override_settings(CRX_ENABLE_ANALYTICS_SETTINGS=False)
    def test_analyticssettings_disabled(self):

        self.assertFalse(self.analytics_settings.enabled())


class DummySettingsObject(SettingsCheckMixin):
    ENABLE_SETTINGS = "CRX_ENABLE_LAYOUT_SETTINGS"


class MaybeRegisterSettingTestCase(WagtailPageTests):
    """Testing the maybe_register_setting decorator.

    These tests use a dummy settings object to test the two paths
    through the decorator which determine whether or not register_settings
    is called."""

    def setUp(self):
        super().setUp()
        self.dummy_settings = DummySettingsObject()

    @patch("coderedcms.models.wagtailsettings_models.register_setting")
    def test_decorator_enabled(self, mock_register_setting):
        """Test that the decorator calls register_setting
        with no override setting (default)."""
        maybe_register_setting(icon="foobar")(self.dummy_settings)
        mock_register_setting.assert_called_once_with(
            self.dummy_settings, icon="foobar"
        )

    @override_settings(CRX_ENABLE_LAYOUT_SETTINGS=False)
    @patch("coderedcms.models.wagtailsettings_models.register_setting")
    def test_decorator_disabled(self, mock_register_setting):
        """Test that the decorator does not call register_setting
        when override setting is False."""
        maybe_register_setting(icon="foobar")(self.dummy_settings)
        mock_register_setting.assert_not_called()
