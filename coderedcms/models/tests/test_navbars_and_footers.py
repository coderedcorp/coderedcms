# what imports do I need?
# possibly use https://pypi.org/project/django-test-migrations/ instead?

import json
from django.apps import apps
from django.test import Client, TestCase
# from django_test_migrations.contrib.unittest_case import MigratorTestCase
from django.db.migrations.executor import MigrationExecutor
from django.db import connection

from wagtail.core.models import Site

from coderedcms.models.wagtailsettings_models import (
    LayoutSettings,
    NavbarOrderable,
    FooterOrderable
)


# Set up
class TestMigrations(TestCase):

    @property
    def app(self):
        return apps.get_containing_app_config(type(self).__module__).name

    migrate_from = None
    migrate_to = None


# Need to create Site that has navbar and footer the current way
class NavsandFootersTestCase(TestMigrations):

    def prepare(self, apps):
        NavbarInitial = Navbar.objects.create(
            name = "Main Nav",
            menu_items = json.dumps[
                {\"type\": \"row\", \"value\": {\"settings\": {\"custom_template\": \"\", \"custom_css_class\": \"\", \"custom_id\": \"\"}, \"fluid\": false, \"content\": [{\"type\": \"content\", \"value\": {\"settings\": {\"custom_template\": \"\", \"custom_css_class\": \"\", \"custom_id\": \"\", \"column_breakpoint\": \"md\"}, \"column_size\": \"\", \"content\": [{\"type\": \"text\", \"value\": \"<h2>Footer Content</h2>\", \"id\": \"5d6be173-bab8-4d2f-93a9-94614267e776\"}]}, \"id\": \"016bdac5-0b6c-484f-ae53-b9ae115d5dd9\"}]}, \"id\": \"0d39786b-e959-4382-898a-20946f979da1\"}
            ]

        )
        FooterInitial = Footer.objects.create(
            name = "Main Footer",
            content = json.dumps[
                {\"type\": \"row\", \"value\": {\"settings\": {\"custom_template\": \"\", \"custom_css_class\": \"\", \"custom_id\": \"\"}, \"fluid\": false, \"content\": [{\"type\": \"content\", \"value\": {\"settings\": {\"custom_template\": \"\", \"custom_css_class\": \"\", \"custom_id\": \"\", \"column_breakpoint\": \"md\"}, \"column_size\": \"\", \"content\": [{\"type\": \"text\", \"value\": \"<h2>Footer Content</h2>\", \"id\": \"5d6be173-bab8-4d2f-93a9-94614267e776\"}]}, \"id\": \"016bdac5-0b6c-484f-ae53-b9ae115d5dd9\"}]}, \"id\": \"0d39786b-e959-4382-898a-20946f979da1\"}
            ]
        )




# Then run the migrations and check if the navbar and footer was added to orderables
