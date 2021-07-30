from django.test import Client
from wagtail.tests.utils import WagtailPageTests
from wagtail.core.models import Site

from coderedcms.tests.testapp.models import WebPage
from coderedcms.models.wagtailsettings_models import AnalyticsSettings


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
        self.settings.ga_tracking_id = "UA-123"
        self.settings.head_scripts = "<script>evil_tracker</script>"
        self.settings.body_scripts = "<script>annoying_tracker</script>"
        self.settings.save()

    def test_get(self):
        """
        Tests to make sure the page serves a 200 from a GET request.
        """
        response = self.client.get(self.homepage.url, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_ga_tracking_id(self):
        """
        Make sure the ga_tracking_id is present.
        """
        response = self.client.get(self.homepage.url, follow=True)
        self.assertIn(self.settings.ga_tracking_id, str(response.content), 1)

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
