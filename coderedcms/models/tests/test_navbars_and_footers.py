# what imports do I need?
# possibly use https://pypi.org/project/django-test-migrations/ instead?

from django.apps import apps
from django.test import Client, TestCase

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


class NavbarTestCase(WagtailPageTests):
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

        # create 1 nav snippet
        self.navbar = Navbar.objects.create(
            name="Nav1",
            custom_id="Nav1"
        )

        # Populate settings.
        self.settings = LayoutSettings.for_site(self.site)
        # layout = self.settings
        self.navbarorderable = NavbarOrderable.objects.create(
            sort_order=0,
            navbar_chooser=LayoutSettings.objects.get(id=self.settings.id),
            navbar=Navbar.objects.get(id=self.navbar.id)
        )
        # get the navbar (orderable)
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
        self.assertIn(f'<ul class="navbar-nav" id="{self.navbar.custom_id}">', str(response.content), 1)
        # set 1 navbar, check that the chosen one is there but not the other

    def test_multi_navbars(self):
        pass
        # update settings for using 2 navs, then check that both navbars show


# # Set up
# class TestMigrations(TestCase):
#     @property
#     def app(self):
#         return apps.get_containing_app_config(type(self).__module__).name

#     migrate_from = None
#     migrate_to = None

#     def setUp(self):
#         assert self.migrate_from and self.migrate_to, \
#             "TestCase '{}' must define migrate_from and migrate_to properties".format(type(self).__name__)
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
#             # menu_items = json.dumps[
#             # {\"type\": \"row\", \"value\": {\"settings\": {\"custom_template\": \"\", \"custom_css_class\": \"\", \"custom_id\": \"\"}, \"fluid\": false, \"content\": [{\"type\": \"content\", \"value\": {\"settings\": {\"custom_template\": \"\", \"custom_css_class\": \"\", \"custom_id\": \"\", \"column_breakpoint\": \"md\"}, \"column_size\": \"\", \"content\": [{\"type\": \"text\", \"value\": \"<h2>Footer Content</h2>\", \"id\": \"5d6be173-bab8-4d2f-93a9-94614267e776\"}]}, \"id\": \"016bdac5-0b6c-484f-ae53-b9ae115d5dd9\"}]}, \"id\": \"0d39786b-e959-4382-898a-20946f979da1\"}
#             # ]
#         ).id
#         Footer = apps.get_model('coderedcms', 'Footer')
#         Footer.id = Footer.objects.create(
#             name="Main Footer",
#             content=StreamField([('text', 'this is a footer')])
#             # content = json.dumps[
#             # {\"type\": \"row\", \"value\": {\"settings\": {\"custom_template\": \"\", \"custom_css_class\": \"\", \"custom_id\": \"\"}, \"fluid\": false, \"content\": [{\"type\": \"content\", \"value\": {\"settings\": {\"custom_template\": \"\", \"custom_css_class\": \"\", \"custom_id\": \"\", \"column_breakpoint\": \"md\"}, \"column_size\": \"\", \"content\": [{\"type\": \"text\", \"value\": \"<h2>Footer Content</h2>\", \"id\": \"5d6be173-bab8-4d2f-93a9-94614267e776\"}]}, \"id\": \"016bdac5-0b6c-484f-ae53-b9ae115d5dd9\"}]}, \"id\": \"0d39786b-e959-4382-898a-20946f979da1\"}
#             # ]
#         ).id

#     def test_navs_footers_migrated(self):
#         NavbarOrderable = apps.get_model('coderedcms', 'NavbarOrderable')
