from django.test import Client
from wagtail.test.utils import WagtailPageTests
from wagtail.models import Site

from coderedcms.tests.testapp.models import WebPage
from coderedcms.models.snippet_models import Footer, Navbar
from coderedcms.models.wagtailsettings_models import (
    LayoutSettings,
    NavbarOrderable,
    FooterOrderable,
)


class NavbarFooterTestCase(WagtailPageTests):
    """
    Test that the relevant navbar chooser settings appear in the homepage HTML.
    """

    model = WebPage

    def setUp(self):
        # HTTP client.
        self.client = Client()

        # Use home page and default site.
        self.site = Site.objects.filter(is_default_site=True)[0]
        self.homepage = WebPage.objects.get(url_path="/home/")

        # create 2 nav snippets
        self.navbar = Navbar.objects.create(name="Nav1", custom_id="Nav1")
        self.navbar2 = Navbar.objects.create(name="Nav2", custom_id="Nav2")
        self.footer = Footer.objects.create(name="Footer1", custom_id="Footer1")
        self.footer2 = Footer.objects.create(
            name="Footer2", custom_id="Footer2"
        )

        # Populate settings.
        self.settings = LayoutSettings.for_site(self.site)
        # layout = self.settings
        self.navbarorderable = NavbarOrderable.objects.create(
            sort_order=0,
            navbar_chooser=LayoutSettings.objects.get(id=self.settings.id),
            navbar=Navbar.objects.get(id=self.navbar.id),
        )
        self.footerorderable = FooterOrderable.objects.create(
            sort_order=0,
            footer_chooser=LayoutSettings.objects.get(id=self.settings.id),
            footer=Footer.objects.get(id=self.footer.id),
        )
        # save settings
        self.settings.save()

    def test_get(self):
        """
        Tests to make sure the page serves a 200 from a GET request.
        """
        response = self.client.get(self.homepage.url, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_navbar(self):
        """
        Make sure navbar is on homepage.
        """
        response = self.client.get(self.homepage.url, follow=True)
        # Checks if specified HTML is within response
        # https://docs.djangoproject.com/en/3.2/topics/testing/tools/#django.test.SimpleTestCase.assertContains
        self.assertContains(
            response,
            text=f'<ul class="navbar-nav" id="{self.navbar.custom_id}">',
            status_code=200,
            html=True,
        )
        self.assertNotContains(
            response,
            text=f'<ul class="navbar-nav" id="{self.navbar2.custom_id}">',
            status_code=200,
            html=True,
        )

    def test_multi_navbars(self):
        """
        Adds another navbar and checks if it shows on page.
        """
        self.navbarorderable2 = NavbarOrderable.objects.create(
            sort_order=1,
            navbar_chooser=LayoutSettings.objects.get(id=self.settings.id),
            navbar=Navbar.objects.get(id=self.navbar2.id),
        )
        # get the navbar (orderable)
        self.settings.save()
        # update settings for using 2 navs, then check that both navbars show and in right order
        response = self.client.get(self.homepage.url, follow=True)
        self.assertContains(
            response,
            text=f'<ul class="navbar-nav" id="{self.navbar.custom_id}">'
            f'</ul><ul class="navbar-nav" id="{self.navbar2.custom_id}">',
            status_code=200,
            html=True,
        )

    def test_footer(self):
        """
        Make sure footer is on homepage.
        """
        response = self.client.get(self.homepage.url, follow=True)

        self.assertContains(
            response,
            text=f'<div id="{self.footer.custom_id}">',
            status_code=200,
            html=True,
        )
        self.assertNotContains(
            response,
            text=f'<div id="{self.footer2.custom_id}">',
            status_code=200,
            html=True,
        )

    def test_multi_footers(self):
        """
        Adds another footer to settings and checks if it shows on page.
        """
        self.footerorderable2 = FooterOrderable.objects.create(
            sort_order=1,
            footer_chooser=LayoutSettings.objects.get(id=self.settings.id),
            footer=Footer.objects.get(id=self.footer2.id),
        )
        # get the footer (orderable)
        self.settings.save()
        # update settings for using 2 footers, then check that both footers show
        response = self.client.get(self.homepage.url, follow=True)
        self.assertContains(
            response,
            text=f'<div id="{self.footer.custom_id}"></div><div id="{self.footer2.custom_id}">',
            status_code=200,
            html=True,
        )
