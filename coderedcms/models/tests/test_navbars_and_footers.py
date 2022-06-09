# what imports do I need?
# possibly use https://pypi.org/project/django-test-migrations/ instead?


from django.test import Client

# from django_test_migrations.contrib.unittest_case import MigratorTestCase
# from django.db.migrations.executor import MigrationExecutor
# from django.db import connection

from wagtail.tests.utils import WagtailPageTests
from wagtail.core.models import Site

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
        self.footer2 = Footer.objects.create(name="Footer2", custom_id="Footer2")

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
            response, text=f'<div id="{self.footer.custom_id}">', status_code=200, html=True
        )
        self.assertNotContains(
            response, text=f'<div id="{self.footer2.custom_id}">', status_code=200, html=True
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


# # Set up
# class TestMigrations(TestCase):
#     @property
#     def app(self):
#         return apps.get_containing_app_config(type(self).__module__).name

#     migrate_from = None
#     migrate_to = None

#     def setUp(self):
#         assert self.migrate_from and self.migrate_to, \
#         "TestCase '{}' must define migrate_from and
#         migrate_to properties".format(type(self).__name__)
#         self.migrate_from = [(self.app, self.migrate_from)]
#         self.migrate_to = [(self.app, self.migrate_to)]
#         executor = MigrationExecutor(connection)
#         old_apps = executor.loader.project_state(self.migrate_from).apps

#         # Reverse to the original migration
#         executor.migrate(self.migrate_from)

#         self.setUpBeforeMigration(old_apps)

#         # Run the migration to test
#         executor = MigrationExecutor(connection)
#         executor.loader.build_graph()  # reload.
#         executor.migrate(self.migrate_to)

#         self.apps = executor.loader.project_state(self.migrate_to).apps


# # Need to create Site that has navbar and footer the current way?
# class NavsandFootersTestCase(TestMigrations):

#     # migrate_from = '0024_analyticssettings'
#     # migrate_to = '0025_multinavs.py'

#     def setUpBeforeMigration(self, apps):
#         # self.site = Site.objects.filter(is_default_site=True)[0]
#         Navbar = apps.get_model('coderedcms', 'Navbar')
#         Navbar.id = Navbar.objects.create(
#             name="Main Nav",
#             menu_items = StreamField([('external_link', 'item1'), ('external_link', 'item2') ])
#             # menu_items = build content here
#         )
#         Footer = apps.get_model('coderedcms', 'Footer')
#         Footer.id = Footer.objects.create(
#             name="Main Footer",
#             content=StreamField([('text', 'this is a footer')])
#             # content = build content here
#         )

#    def t_navs_footers_migrated(self):
#           NavbarOrderable = apps.get_model('coderedcms', 'NavbarOrderable')
